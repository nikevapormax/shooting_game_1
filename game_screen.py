import pygame
import sys  # 파이썬 인터프리터가 제공하는 변수와 함수를 직접 제어할 수 있게 해주는 모듈
import random
from time import sleep  # 일정 시간동안 프로세스를 일시정지할 수 있음 / sleep(10) -> 10초간 프로세스 중지

# 게임 전체 화면 크기 및 전체 배경
BLACK = (0, 0, 0)  # 배경화면 RGB값
padWidth = 480  # 가로
padHeight = 640  # 세로
rock_image = ['rock01.png', 'rock02.png', 'rock03.png', 'rock04.png', 'rock05.png', 'rock06.png',
              'rock07.png', 'rock08.png', 'rock09.png', 'rock10.png', 'rock11.png', 'rock12.png',
              'rock13.png', 'rock14.png', 'rock15.png', 'rock16.png', 'rock17.png', 'rock18.png',
              'rock19.png', 'rock20.png', 'rock21.png', 'rock22.png', 'rock23.png', 'rock24.png',
              'rock25.png', 'rock26.png', 'rock27.png', 'rock28.png', 'rock29.png', 'rock30.png'
              ]
explosion_sound = ['explosion01.wav', 'explosion02.wav', 'explosion03.wav', 'explosion04.wav']


def write_score(count): # 파괴한 운석 수 써주는 함수
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20) # 폰트로 나눔고딕을 사용하고 사이즈는 20
    text = font.render(f'파괴한 운석 수 : {count}', True, (255, 255, 255)) # 파괴한 운석 수를 흰색 글씨하고 이것을 폰트에 렌더링해서 변수 text에 저장
    gamePad.blit(text, (10, 0))     # blit 함수를 통해 게임패드의 좌상단 쪽에 변수 text의 내용을 보여줌


def write_passed(count): # 운석이 화면 아래로 통과한 개수
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20) # 폰트로 나눔고딕을 사용하고 사이즈는 20
    text = font.render(f'놓친 운석 수 : {count}', True, (255,0,0))
    gamePad.blit(text, (340, 0))


def write_massage(text):
    global gamePad, gameoverSound
    textfont = pygame.font.Font('NanumGothic.ttf', 80)
    text = textfont.render(text, True, (255, 0, 0))
    textpos = text.get_rect()                       # 텍스트 포지션의 값을 텍스트의 포지션으로 잡고
    textpos.center = (padWidth / 2, padHeight / 2)  # 텍스트포지션의 중앙값을 게임창의 중앙 좌표로 잡아주고
    gamePad.blit(text, textpos)     # 실제 화면에 textpos의 위치에 text를 띄워줌
    pygame.display.update()    # 게임오버니까 게임 화면을 처음 상태로 다시 그려줌
    pygame.mixer.music.stop()   # 배경음악 나오는거 탈락이니까 끄고
    game_over_sound.play()      # 게임오버 사운드 틀어주기
    sleep(2)                    # 2초간 화면 멈추고
    pygame.mixer.music.play(-1)  # 배경음악 다시 틀어주고(-1이 뭐라고? 무한 반복)
    run_game()                  # 게임 다시 틀고


def crush():  # 전투기와 운석이 충돌했을 때의 메시지 출력
    global gamePad
    write_massage('전투기 파괴')


def game_over():    # 게임오버 메시지 출력
    global gamePad
    write_massage('게임 오버!')


# 게임에 등장하는 객체를 그려줌
def draw_object(obj, x, y):  # 요고는 내가 만든 함수명일뿐
    global gamePad
    gamePad.blit(obj, (x, y))  # 게임패드에 blit하라는 뜻으로, 화면에 obj를 표시하는데 그 위치는 (x, y)이다.


def init_game():  # 게임을 만들기 위해 초기화 해주는 함수
    global gamePad, clock, background, plane, missile, explosion, missile_sound, game_over_sound
    pygame.init()  # 파이게임 초기화(무엇인가를 사용하려면 꼭 초기화를 시켜야 함)
    gamePad = pygame.display.set_mode((padWidth, padHeight))  # 게임패드의 크기를 전체 화면의 크기로 설정
    pygame.display.set_caption('SHOOT THE ROCK')  # 게임 이름 설정
    background = pygame.image.load('img/background.png')  # 배경 그림을 가져옴
    plane = pygame.image.load('img/fighter.png')  # 전투기 사진 가져옴
    missile = pygame.image.load('img/missile.png')  # 미사일 사진 가져옴
    explosion = pygame.image.load('img/explosion.png')  # 폭파되는 사진 가져옴

    pygame.mixer.music.load('music.wav')    # 배경음악 가져옴
    pygame.mixer.music.play(-1)             # play(-1)은 무한반복 의미
    missile_sound = pygame.mixer.Sound('missile.wav')    # 미사일 발사 사운드
    game_over_sound = pygame.mixer.Sound('gameover.wav') # 게임오버 사운드드

    clock = pygame.time.Clock() # 시간을 추적하는데 도움이 되는 개체 만들기


def run_game():
    global gamePad, clock, background, plane, missile, explosion, missile_sound

    # 전투기의 크기 조정
    plane_size = plane.get_rect().size  # 게임 객체(rect) : 크기 정보 + 좌표 정보 보유 / 그러니까 결국 상세한 좌표대신 2D 게임이므로 사각형을 쓰는거
    plane_width = plane_size[0]  # rect 값을 받아오면 [가로, 세로] 길이의 형태로 들어오기 때문에 이와 같이 설정
    plane_height = plane_size[1]

    # 전투기 초기 위치 설정 (x, y)
    x = padWidth * 0.45  # 게임 창의 폭의 0.45가 되는 위치
    y = padHeight * 0.9  # 게임 창의 높이에서 0.9가 되는 위치 => 즉 게임 화면 하단의 중간
    planeX = 0

    # 무기 좌표 리스트
    missileXY = []

    rock = pygame.image.load(random.choice(rock_image))  # 운석 이미지를 랜덤하게 rock_image에서 가져와서 rock 변수 안에 저장
    # 운석 크기
    rock_size = rock.get_rect().size  # 게임 객체(rect) : 크기 정보 + 좌표 정보 보유 / 그러니까 결국 상세한 좌표대신 2D 게임이므로 사각형을 쓰는거
    rock_width = rock_size[0]  # rect 값을 받아오면 [가로, 세로] 길이의 형태로 들어오기 때문에 이와 같이 설정
    rock_height = rock_size[1]
    destroy_sound = pygame.mixer.Sound(random.choice(explosion_sound))
    # 운석의 초기 위치를 설정하는데, 이거는 랜덤하게 갑니다
    rockX = random.randrange(0, padWidth - rock_width)  # 운석이 화면 밖으로 나가면 안되니까 전체 가로에서 운석 가로 빼줌
    rockY = 0  # 맨 위에서 떨어지니까; 맨위의 Y 좌표값은 0이다! 왜냐면 좌상단 끝점이 (0, 0) 이니까
    rockSpeed = 2  # 운석 스피드

    # 전투기 미사일에 운석이 맞았을 때 -> True
    is_shot = False
    shot_count = 0   # 맞은거 카운트
    rock_passed = 0  # 운석을 놓쳤을 때 카운트

    on_game = False
    while not on_game:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:  # 게임 프로그램 종료
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:  # 키보드를 눌러 키보드 이벤트가 발생했을 때 전투기의 위치가 얼마나 바뀔지 설정
                if event.key == pygame.K_LEFT:  # 전투기가 키보드 왼쪽 방향키를 누르게 되면 왼쪽으로 이동
                    planeX -= 5
                elif event.key == pygame.K_RIGHT:  # 전투기가 키보드 오른쪽 방향키를 누르게 되면 오른쪽으로 이동
                    planeX += 5
                elif event.key == pygame.K_SPACE:  # 스페이스바 키보드 이벤트를 일으켜 미사일 발사
                    missile_sound.play()
                    missileX = x + plane_width / 2  # 미사일이 비행기의 중앙에서 나갈 수 있도록(비행기의 좌표는 왼쪽이다)
                    missileY = y - plane_height  # 미사일이 비행기의 코에서 나갈 수 있도록 전체에서 비행기만큼의 길이를 제외
                    missileXY.append([missileX, missileY])  # 미사일의 좌표값에 해당 위치들을 저장

            if event.type in [pygame.KEYUP]:  # 키보드의 방향키를 떼면 전투기가 멈춤!
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    planeX = 0

        draw_object(background, 0, 0)  # 배경화면의 위치를 설정했는데, 게임창 좌상단인 (0, 0)에 위치시켰고, 이러면 화면 전체에 적용됨

        # 전투기의 좌표를 다시 재조정해주는 것(위의 키보드 이벤트에 영향받은 것을)
        x += planeX
        if x < 0:  # 왼쪽 화면 끝까지 갔을 때이다.
            x = 0  # 이렇게 해서 전투기가 화면 밖으로 나가지 않도록 할 수 있음
        elif x > padWidth - plane_width:  # 오른쪽 화면 끝까지 갔을 때
            x = padWidth - plane_width  # 비행기의 좌표는 비행기 그림 왼쪽에 있기 때문에 해당 좌표가 전체 가로에서 비행기 가로 길이를 뺀 값을 넘어가면 그림이 화면을 벗어남

        # 전투기가 운석과 충돌했는지 체크
        if y < rockY + rock_height:
            if (rockX > x and rockX < x + plane_width) or (rockX + rock_width > x and rockX + rock_width < x + plane_width):
                crush()

        draw_object(plane, x, y)  # 전투기를 게임 화면의 (x, y) 좌표에 그림

        # 미사일 발사 화면에 그리기
        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):  # 미사일 요소를 반복
                bxy[1] -= 10  # 미사일의 (y좌표 - 10), 즉 미사일이 위로 이동하게 됨
                missileXY[i][1] = bxy[1]  # 미사일이 쏴진만큼 원래 리스트 값에서 갱신 진행

                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] < rockX + rock_width: # 미사일이 운석의 범위 안에 들어옴
                        missileXY.remove(bxy)       # 미사일이랑 돌이랑 만났으니까 미사일 삭제
                        is_shot = True              # 이게 참으로 바뀌고
                        shot_count += 1             # 샷카운트 하나 올려줌

                if bxy[1] <= 0:  # 미사일이 천장을 벗어나면?
                    try:
                        missileXY.remove(bxy)  # 미사일 제거
                    except:
                        pass

        if len(missileXY) != 0:
            for bx, by in missileXY:
                draw_object(missile, bx, by)

        write_score(shot_count) # 바로 윗부분에 있는 샷카운트가 미사일로 운석을 맞혀 반영이 되었으니 여기서 화면에 나타나도록 조치해줌

        rockY += rockSpeed  # 운석이 아래로 움직임
        # 운석이 지구로 떨어진 경우
        if rockY > padHeight:  # 즉, 운석의 스피드가 중첩되서 rockY, 즉 운석의 y좌표가 화면의 길이보다 커져 화면 밖으로 나갈 때
            # 새로운 운석 랜덤하게 생성
            rock = pygame.image.load(random.choice(rock_image))
            rock_size = rock.get_rect().size
            rock_width = rock_size[0]
            rock_height = rock_size[1]
            rockX = random.randrange(0, padWidth - rock_width)  # 운석이 화면 밖으로 나가면 안되니까 전체 가로에서 운석 가로 빼줌
            rockY = 0  # 맨 위에서 떨어지니까; 맨위의 Y 좌표값은 0이다! 왜냐면 좌상단 끝점이 (0, 0) 이니까
            rock_passed += 1 # 운석이 지구에 그대로 떨어졌으니까 지나간거 하나 더해줌
        
        # 만약 놓친 운석의 수가 3개라면 게임오버
        if rock_passed == 3:
            game_over()

        write_passed(rock_passed) # 바로 윗부분에 있는 패스카운트가 운석이 바닥에 닿아 반영이 되었으니 여기서 화면에 나타나도록 조치해줌

        if is_shot: # 운석이랑 미사일이 맞게되면
            draw_object(explosion, rockX, rockY)    # 운석을 폭파하고 폭발 사진을 그려줌
            destroy_sound.play()        # 운석 폭발음 재생
            # 새로운 운석을 그려줌
            rock = pygame.image.load(random.choice(rock_image))
            rock_size = rock.get_rect().size
            rock_width = rock_size[0]
            rock_height = rock_size[1]
            rockX = random.randrange(0, padWidth - rock_width)  # 운석이 화면 밖으로 나가면 안되니까 전체 가로에서 운석 가로 빼줌
            rockY = 0  # 맨 위에서 떨어지니까; 맨위의 Y 좌표값은 0이다! 왜냐면 좌상단 끝점이 (0, 0) 이니까
            destroy_sound = pygame.mixer.Sound(random.choice(explosion_sound))  # 운석이 부서지는 소리를 가져옴
            is_shot = False
            
            # 자 이제 운석을 맞춘거니까 난이도 조절 들어갑니다~
            rockSpeed += 0.2   # 운석의 속도를 찔끔찔끔 올리는데
            if rockSpeed >= 10: # 운석이 또 너무 빠르면 답이 없으니까
                rockSpeed = 10  # 운석 속도를 최대 10으로 제한하자


        draw_object(rock, rockX, rockY)  # 운석 그려주기

        pygame.display.update()  # 게임 화면을 다시 그려줌
        clock.tick(60)  # 게임의 초당 프레임을 60으로 설정

    pygame.quit()  # 파이게임 종료


init_game()
run_game()
