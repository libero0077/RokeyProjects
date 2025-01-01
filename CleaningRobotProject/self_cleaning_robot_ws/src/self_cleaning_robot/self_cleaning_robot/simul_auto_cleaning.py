import yaml
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import heapq
from collections import deque
from matplotlib import animation

#####################################
# 1. YAML & 맵 로드
#####################################
def read_yaml(yaml_path):
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)

def load_map(pgm_path):
    img = cv2.imread(pgm_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Map not found: {pgm_path}")
    return img

#####################################
# 2. 벽 회피 BFS로 "실제 맨해튼 최단 경로 비용" 계산
#####################################
def manhattan_bfs(original_map, start):
    """
    - original_map[y,x] == 0 => 벽, 이동 불가
    - 4방향 BFS, distance_map[y,x] = start->(x,y)까지 최소 맨해튼 비용(실제 이동)
    - 이동 불가시 inf
    """
    h,w= original_map.shape
    dist_map= np.full((h,w), np.inf, dtype=float)

    sx,sy= start
    if original_map[sy,sx]==0:
        return dist_map  # 시작이 벽이면 불가능

    dist_map[sy,sx]=0
    queue=deque()
    queue.append((sx,sy))

    while queue:
        x,y= queue.popleft()
        cost= dist_map[y,x]
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx,ny= x+dx,y+dy
            if 0<=nx<w and 0<=ny<h:
                if original_map[ny,nx]==0:
                    continue
                if dist_map[ny,nx]> cost+1:
                    dist_map[ny,nx]= cost+1
                    queue.append((nx,ny))

    return dist_map

#####################################
# 3. "가장 가까운 라인 끝" 찾기
#####################################
def find_closest_line_end_bfs(robot_pos, lines, original_map):
    """
    BFS dist_map[y,x] 에서 라인 양끝점 중 최소값 찾기
    반환: (chosen_line, chosen_end)
    """
    dist_map= manhattan_bfs(original_map, robot_pos)
    h,w= dist_map.shape

    chosen_line=None
    chosen_end=None
    min_dist= float('inf')

    for ln in lines:
        (x1,y1),(x2,y2)= ln
        if 0<=x1<w and 0<=y1<h:
            d1= dist_map[y1,x1]
            if d1< min_dist:
                min_dist= d1
                chosen_line= ln
                chosen_end= (x1,y1)
        if 0<=x2<w and 0<=y2<h:
            d2= dist_map[y2,x2]
            if d2< min_dist:
                min_dist= d2
                chosen_line= ln
                chosen_end= (x2,y2)

    if min_dist== float('inf'):
        return None,None
    return chosen_line, chosen_end

#####################################
# 4. 메인 라인 생성 및 필터
#####################################
def generate_horizontal_lines(map_img, offset_px, free_space_threshold=250):
    h,w= map_img.shape
    lines=[]
    _, binmap= cv2.threshold(map_img, free_space_threshold, 255, cv2.THRESH_BINARY)
    for y in range(0,h,offset_px):
        row= binmap[y,:]
        in_free=False
        start_x=0
        for x in range(w):
            if row[x]==255 and not in_free:
                in_free=True
                start_x=x
            elif row[x]==0 and in_free:
                in_free=False
                lines.append(((start_x,y),(x-1,y)))
        if in_free:
            lines.append(((start_x,y),(w-1,y)))
    return lines

def remove_close_pixels(map_img, lines, offset_px):
    """
    offset_px+2 이상 거리 유지
    """
    _, binmap= cv2.threshold(map_img,250,255,cv2.THRESH_BINARY)
    distmap= cv2.distanceTransform(binmap,cv2.DIST_L2,5).astype(np.int32)

    extra= offset_px+2
    filtered=[]
    for (x1,y),(x2,y) in lines:
        if x1<0 or x2<0 or x2<x1 or x2>=distmap.shape[1]:
            continue
        rowdist= distmap[y, x1:x2+1]
        valid= np.where(rowdist>= extra)[0]
        if valid.size>0:
            splits= np.split(valid, np.where(np.diff(valid)!=1)[0]+1)
            for s in splits:
                if s.size>0:
                    ns= x1+ s[0]
                    ne= x1+ s[-1]
                    filtered.append(((ns,y),(ne,y)))
    return filtered

#####################################
# 5. 외곽 라인(벽 offset) - 자유구역 기반 폐곡선 방식
#####################################
def generate_wall_offset_lines(map_img, offset_px):
    """
    내부 벽(홀) 포함한 모든 벽(바깥+내부)로부터 offset_px 이상 떨어진 자유공간의 윤곽선을 찾는다.
    1) 이진화 (자유=255, 벽=0)
    2) distanceTransform
    3) dist >= offset_px 인 영역만 255, 나머지는 0
    4) findContours(..., RETR_TREE, CHAIN_APPROX_SIMPLE) => 내부 홀 포함
    5) 윤곽선(폐곡선) 리스트 반환
    """
    # 1) 이진화
    _, binmap = cv2.threshold(map_img, 250, 255, cv2.THRESH_BINARY)

    # 2) distanceTransform
    distmap = cv2.distanceTransform(binmap, cv2.DIST_L2, 5).astype(np.float32)

    # 3) dist >= offset_px => 255, else 0
    safe_mask = np.zeros_like(distmap, dtype=np.uint8)
    safe_mask[distmap >= offset_px] = 255  # offset_px 이상인 곳만 남김

    # 4) 윤곽선 탐색: 내부/외부 벽 모두 인식하기 위해 RETR_TREE 사용
    contours, hierarchy = cv2.findContours(safe_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 윤곽선 = contours[i], 각각 (N, 1, 2) shape => (x, y)
    # 외곽 라인을 polygon(폐곡선) 형태로 저장
    offset_polygons = []
    for cnt in contours:
        # cnt : shape (N, 1, 2)
        cnt_xy = cnt.reshape(-1, 2)  # (N,2)
        offset_polygons.append(cnt_xy)

    return offset_polygons

def generate_wall_offset_segments(map_img, offset_px):
    """
    1) 'generate_wall_offset_lines' 함수로 폴리곤(윤곽) 리스트를 얻는다.
       내부 벽(홀) 포함한 모든 외곽 윤곽을 각각 shape=(N,2) 배열로 반환.
    2) 각 폴리곤(폐곡선)을 '연속된 점'들로 순회하며 ( (x1,y1), (x2,y2) ) 형태의
       세그먼트 리스트로 변환.
    3) 세그먼트 리스트를 반환 => build_outer_path_bfs(...) 에서 그대로 사용 가능.
    """
    # (A) 폴리곤(윤곽) 리스트 얻기
    polygons = generate_wall_offset_lines(map_img, offset_px)  
    segment_lines = []

    # (B) 각 폴리곤을 세그먼트들로 쪼갠다.
    for poly in polygons:  # poly shape = (N, 2)
        n = len(poly)
        if n < 2:
            continue
        # 폐곡선으로 취급: i→i+1, 그리고 마지막→첫점 닫기
        for i in range(n):
            x1, y1 = poly[i]
            x2, y2 = poly[(i+1) % n]  # (i+1)%n: 마지막→첫점 닫기
            segment_lines.append(((x1, y1), (x2, y2)))

    return segment_lines

#####################################
# 5.1 외곽선 시각화 (폐곡선 방식)
#####################################
def visualize_wall_offset_polygons(map_img, offset_polygons):
    fig, ax = plt.subplots(figsize=(10,10))
    ax.imshow(map_img, cmap='gray')
    for poly in offset_polygons:
        x = poly[:,0]
        y = poly[:,1]
        # 폐곡선 형태이므로 plt.plot + 마지막 점->첫 점 닫아줄 수도 있음
        ax.plot(x, y, color='orange', linewidth=2)
        # 만약 선을 닫고 싶다면
        ax.plot([x[-1], x[0]], [y[-1], y[0]], color='orange', linewidth=2)
    ax.set_title("Offset Polygons (Including Interior Walls)")
    ax.invert_yaxis()
    plt.show()

#####################################
# 6. 메인 라인 연결
#####################################
def build_main_path_bfs(main_lines, start_pos, original_map):
    """
    1) BFS(맨해튼)로 가장 가까운 라인 끝 -> 직선 '점선' 연결
    2) 라인 반대 끝으로 이동, 라인 제거
    3) 모든 라인 연결 -> 마지막 위치 반환
    """
    remain= main_lines.copy()
    connected_lines=[]
    dashed_connects=[]  # 점선(빨강)

    current= start_pos
    while remain:
        line, end= find_closest_line_end_bfs(current, remain, original_map)
        if not line:
            break

        # "점선 연결"
        dashed_connects.append((current, end, 'red'))  # (start->end, color='red')
        connected_lines.append(line)
        remain.remove(line)

        # 라인 반대끝
        if end== line[0]:
            current= line[1]
        else:
            current= line[0]

    return connected_lines, dashed_connects, remain, current

#####################################
# 7. 외곽 라인 연결
#####################################
def build_outer_path_bfs(outer_lines, start_pos, original_map):
    """
    "한번 연결되면 그 라인을 끝까지" → 
    BFS로 가장 가까운 라인 끝 -> 점선(보라) 연결 -> 라인 반대끝도 이어 "한 바퀴"
    """
    remain= outer_lines.copy()
    connected_lines=[]
    dashed_connects=[]
    current= start_pos

    while remain:
        line, end= find_closest_line_end_bfs(current, remain, original_map)
        if not line:
            break

        # 점선(보라)
        dashed_connects.append((current,end,'purple'))
        connected_lines.append(line)
        remain.remove(line)

        # "한 바퀴": end->other_end도 연결
        if end== line[0]:
            other_end= line[1]
        else:
            other_end= line[0]
        dashed_connects.append((end, other_end, 'purple'))

        current= other_end

    return connected_lines, dashed_connects, remain, current

#####################################
# 8. 복귀 (점선, 흰색)
#####################################
def return_to_start_bfs(current_pos, start_pos):
    """
    마지막 위치->시작 위치, 점선(흰색)으로 연결
    (벽 피해서 BFS로 실제 거리가 가능하면 "가장 가까움"?
     요구대로 그냥 연결?)
    여기선 그냥 직선 점선(흰색)
    """
    if current_pos== start_pos:
        return []
    return [ (current_pos, start_pos, 'white') ]

#####################################
# 9. 최종 시각화 + 애니메이션
#####################################
def visualize_everything(original_map,
                         main_lines, main_dashed, remain_main,
                         outer_lines, outer_dashed, remain_outer,
                         return_line,
                         start_pos):
    """
    - main_lines: 파랑 실선
    - main_dashed(빨강 점선)
    - outer_lines: 주황 실선
    - outer_dashed(보라 점선)
    - return_line: 흰색 점선
    - 최종 경로 따라 로봇 이동
    """
    fig, ax= plt.subplots(figsize=(10,10))
    ax.imshow(original_map, cmap='gray')

    # 1) 메인 라인(파랑 실선)
    for ln in main_lines:
        (x1,y1),(x2,y2)= ln
        ax.plot([x1,x2],[y1,y2],color='blue',linewidth=2,
                label='Main Line' if 'Main Line' not in ax.get_legend_handles_labels()[1] else "")

    # 남은 메인(빨강 실선)
    for ln in remain_main:
        (x1,y1),(x2,y2)= ln
        ax.plot([x1,x2],[y1,y2],color='tomato',linewidth=1,
                label='Remain Main' if 'Remain Main' not in ax.get_legend_handles_labels()[1] else "")

    # 2) 메인 라인 "점선 연결"(빨강)
    #   (start->end, color='red')
    #   => 이들을 하나의 "경로"로 합쳐서 순서대로 로봇이 이동할 path 구성
    dashed_paths=[]

    for (sx,sy,c) in []: 
        pass
    # We'll build final_path after we plot

    for (sx,sy,col) in []:
        pass

    # main_dashed
    # outer_dashed
    # return_line
    # let's store them in final_dashed

    final_dashed= main_dashed + outer_dashed + return_line  # all dashed lines in order

    # plot dashed lines
    for (sx,sy,color) in []:
        pass

    # Actually we want to keep not just (sx,sy,color) but (sx,sy, ex,ey, color).
    # We'll store them as: ( (sx,sy), (ex,ey), color ).
    for (spos, epos, col) in main_dashed:
        (sx,sy)= spos
        (ex,ey)= epos
        ax.plot([sx,ex],[sy,ey],'--',color=col,linewidth=2,
                label='Main Connect' if col=='red' and 'Main Connect' not in ax.get_legend_handles_labels()[1] else "")

    # 3) 외곽 라인(주황 실선)
    for ln in outer_lines:
        (x1,y1),(x2,y2)= ln
        ax.plot([x1,x2],[y1,y2],color='orange',linewidth=2,
                label='Outer Line' if 'Outer Line' not in ax.get_legend_handles_labels()[1] else "")

    # 남은 외곽(갈색 실선)
    for ln in remain_outer:
        (x1,y1),(x2,y2)= ln
        ax.plot([x1,x2],[y1,y2],color='brown',linewidth=1,
                label='Remain Outer' if 'Remain Outer' not in ax.get_legend_handles_labels()[1] else "")

    # 4) 외곽 라인 점선(보라)
    for (spos, epos, col) in outer_dashed:
        (sx,sy)= spos
        (ex,ey)= epos
        ax.plot([sx,ex],[sy,ey],'--',color=col,linewidth=2,
                label='Outer Connect' if col=='purple' and 'Outer Connect' not in ax.get_legend_handles_labels()[1] else "")

    # 5) 복귀(흰색 점선)
    for (spos, epos, col) in return_line:
        (sx,sy)= spos
        (ex,ey)= epos
        ax.plot([sx,ex],[sy,ey],'--',color=col,linewidth=2,
                label='Return Path' if col=='white' and 'Return Path' not in ax.get_legend_handles_labels()[1] else "")

    # 로봇 시작점
    ax.plot(start_pos[0],start_pos[1],'ro',markersize=8,label='Robot Start')

    ax.set_title("Complete Path:\n"
                 "1) All main lines (blue) + main connect (red dashed)\n"
                 "2) Outer lines (orange) + outer connect (purple dashed)\n"
                 "3) Return path (white dashed)\n"
                 "BFS(4-dir) to find nearest line, direct dashed line to connect.")
    ax.set_xlabel("X (pixels)")
    ax.set_ylabel("Y (pixels)")
    ax.invert_yaxis()

    # 범례
    hds,lbs= ax.get_legend_handles_labels()
    uniq= dict(zip(lbs,hds))
    ax.legend(uniq.values(), uniq.keys(), loc='upper right')

    # ---- 최종 경로(로봇 애니메이션) ----
    # 사용자가 "모든 선 연결 + 외곽 선 한바퀴 + 복귀"를 하나의 완성 경로로 보고 싶어함
    # => main_dashed + outer_dashed + return_line 순서대로 연결해서 path

    # 1) build path from main_dashed lines (in order)
    final_robot_path=[]
    current= start_pos

    # helper: interpolate dashed
    def interpolate_dashed(spos, epos):
        # simple linear interpolation
        (sx,sy)= spos
        (ex,ey)= epos
        points=[]
        steps= max(abs(ex-sx), abs(ey-sy))
        if steps==0:
            return [spos]
        dx= (ex-sx)/steps
        dy= (ey-sy)/steps
        for i in range(steps+1):
            xx= int(sx+ dx*i)
            yy= int(sy+ dy*i)
            points.append((xx,yy))
        return points

    # (A) 메인 dashed
    for (spos, epos, col) in main_dashed:
        # assume we do them in order => BFS picking ensures the sequence?
        # might not be 100% sorted in time, but let's just assume
        # we'll do them in the appended order
        final_robot_path+= interpolate_dashed(spos, epos)
        current= epos
    # (B) 외곽 dashed
    for (spos, epos, col) in outer_dashed:
        final_robot_path+= interpolate_dashed(spos, epos)
        current= epos
    # (C) return line
    for (spos, epos, col) in return_line:
        final_robot_path+= interpolate_dashed(spos, epos)
        current= epos

    # 로봇 그리기
    robot_marker,= ax.plot([],[],'yo',markersize=10,label='Robot')
    robot_route,= ax.plot([],[],'y-',linewidth=2,label='Robot Route')

    # 애니메이션
    def init():
        robot_marker.set_data([],[])
        robot_route.set_data([],[])
        return robot_marker, robot_route

    def animate(i):
        if i< len(final_robot_path):
            (rx,ry)= final_robot_path[i]
            robot_marker.set_data(rx,ry)
            rxs,rys= zip(*final_robot_path[:i+1])
            robot_route.set_data(rxs,rys)
        return robot_marker, robot_route

    anim= animation.FuncAnimation(fig,animate,init_func=init,
                                  frames=len(final_robot_path),
                                  interval=50, blit=False, repeat=False)

    plt.show()

###################################
# 10. 메인
###################################
def main():
    yaml_path= "/home/yjh/Doosan/Real_project_ws/Week8/self_cleaning_robot_ws/src/self_cleaning_robot/self_cleaning_robot/map.yaml"
    if not os.path.exists(yaml_path):
        print("YAML file not found:",yaml_path)
        return
    data= read_yaml(yaml_path)
    if data is None:
        return

    pgm_path= os.path.join(os.path.dirname(yaml_path), data["image"])
    if not os.path.exists(pgm_path):
        print("Map file not found:",pgm_path)
        return

    # (A) 맵 로드
    original_map= load_map(pgm_path)

    # (B) 해상도
    resolution= data.get('resolution',0.05)
    print("Resolution:", resolution)

    offset_m= 0.2
    offset_px= int(offset_m/resolution)
    print(f"Offset: {offset_m}m -> {offset_px}px")

    # (C) 메인 라인
    raw_lines= generate_horizontal_lines(original_map, offset_px)
    main_lines= remove_close_pixels(original_map, raw_lines, offset_px)

    # (D) 외부 및 내부 벽의 offset 외곽선 생성
    outer_polygons = generate_wall_offset_lines(original_map, offset_px)
    outer_segments = generate_wall_offset_segments(original_map, offset_px)  

    # (E) 두 외곽선 시각화
    visualize_wall_offset_polygons(original_map, outer_polygons)

    # 로봇 시작
    robot_start=(200,150)

    # 1) 메인 라인 연결 (BFS + 직선점선)
    c_main_lines, c_main_dashed, remain_main, last_main_pos= build_main_path_bfs(
        main_lines, robot_start, original_map
    )
    print("[MAIN] lines:",len(c_main_lines), "remain:",len(remain_main),
          " last:", last_main_pos)

    # 2) 외곽 라인 연결 => BFS + 직선점선(보라), "한 번 연결되면 한 바퀴"
    c_outer_lines, c_outer_dashed, remain_outer, last_outer_pos= build_outer_path_bfs(
        outer_segments, last_main_pos, original_map
    )
    print("[OUTER] lines:",len(c_outer_lines)," remain:",len(remain_outer),
          " last:", last_outer_pos)

    # 3) 시작 위치 복귀 => 점선(흰색)
    return_line= return_to_start_bfs(last_outer_pos, robot_start)

    # 시각화
    visualize_everything(
        original_map,
        c_main_lines, c_main_dashed, remain_main,
        c_outer_lines, c_outer_dashed, remain_outer,
        return_line,
        robot_start
    )

if __name__=="__main__":
    main()
