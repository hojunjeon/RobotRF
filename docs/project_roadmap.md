# Robot Sorting RL 비전공자용 프로젝트 로드맵

## 이 프로젝트를 한 문장으로 설명하면

컴퓨터 안의 가상 로봇에게 "물건을 집어서 알맞은 박스에 넣는 방법"을 반복 연습시켜서, 나중에는 스스로 분류하도록 만드는 프로젝트다.

여기서 중요한 흐름은 다음과 같다.

1. 내 컴퓨터에서 실행 환경을 만든다.
2. 로봇 시뮬레이션 프로그램을 설치하고 켜 본다.
3. 로봇이 연습할 간단한 상황을 만든다.
4. 강화학습으로 로봇을 훈련한다.
5. 훈련된 모델 파일을 저장한다.
6. 저장한 모델을 다시 불러와서 잘 작동하는지 확인한다.
7. 결과 영상, 그래프, 수치를 모아서 포트폴리오 자료로 정리한다.

## 용어를 쉽게 정리

- 환경: 로봇이 연습하는 가상 공간이다. 책상, 물건, 박스, 로봇 손 같은 것이 들어 있다.
- 시뮬레이션: 실제 로봇 없이 컴퓨터 안에서 로봇을 움직여 보는 프로그램이다.
- 강화학습: 로봇이 행동을 해 보고, 잘하면 보상을 받고, 못하면 다시 시도하면서 배우는 방식이다.
- 모델: 로봇이 연습해서 얻은 행동 규칙 파일이다. 게임의 세이브 파일처럼 저장하고 다시 불러올 수 있다.
- 학습: 모델을 만드는 과정이다.
- 평가: 저장된 모델을 다시 불러와서 정말 잘하는지 시험하는 과정이다.
- 체크포인트: 학습 중간 또는 끝에 저장한 모델 파일이다.
- 로그: 학습이 어떻게 진행됐는지 남긴 기록이다.
- 영상: 로봇이 실제로 물건을 옮기는 모습을 보여주는 결과물이다.

## 전체 단계 요약

| 단계 | 쉬운 이름 | 이 단계에서 하는 일 |
| --- | --- | --- |
| 0 | 개발 환경 만들기 | Python, 가상환경, 필요한 프로그램을 설치한다. |
| 1 | 시뮬레이션 준비 | 로봇이 움직일 가상 환경이 실행되는지 확인한다. |
| 2 | 첫 번째 미션 만들기 | 물건 1개를 박스 1개에 넣는 간단한 문제를 만든다. |
| 3 | 첫 번째 모델 학습 | 로봇에게 첫 번째 미션을 짧게 연습시킨다. |
| 4 | 모델 저장과 로드 | 학습된 모델 파일을 저장하고 다시 불러온다. |
| 5 | 두 번째 미션 만들기 | 물건 종류에 따라 3개 박스 중 맞는 곳에 넣게 한다. |
| 6 | 긴 학습 실행 | 더 오래 학습해서 실제 성공률을 확인한다. |
| 7 | 영상과 그래프 정리 | 결과를 포트폴리오로 보여줄 자료로 만든다. |
| 8 | 고도화 | 더 실제 같은 로봇 환경이나 다른 알고리즘을 실험한다. |

## 0단계: 개발 환경 만들기

목표: 내 컴퓨터에서 이 프로젝트를 실행할 준비를 한다.

해야 할 일:

- Python이 설치되어 있는지 확인한다.
- 프로젝트 전용 가상환경 `.venv`를 만든다.
- 필요한 라이브러리를 설치한다.
- Windows에서 먼저 짧은 테스트가 되는지 확인한다.
- 문제가 생기면 어떤 명령에서 막혔는지 기록한다.

실행할 명령:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_windows_bootstrap.ps1
.\.venv\Scripts\python.exe -m pip install -e .[dev]
.\.venv\Scripts\python.exe scripts\check_runtime.py
.\.venv\Scripts\python.exe -m pytest
```

이 단계가 끝났다는 기준:

- Python과 `.venv`가 정상 작동한다.
- 필요한 프로그램들이 import 된다.
- 테스트 명령이 실행된다.

주의:

- 지금 가장 먼저 해결해야 할 문제는 로컬 Python 환경이다.
- Python이 깨져 있으면 학습, 평가, 모델 로드가 모두 불가능하다.

## 1단계: 강화학습 시뮬레이션 프로그램 설치

목표: 로봇이 연습할 수 있는 가상 프로그램을 준비한다.

이 프로젝트에서 쓰는 주요 프로그램:

- Gymnasium: 강화학습 환경을 만들기 위한 기본 도구.
- Gymnasium-Robotics: 로봇 강화학습 환경을 위한 도구.
- MuJoCo: 로봇이나 물체 움직임을 물리적으로 시뮬레이션하는 도구.
- Stable-Baselines3: 강화학습 모델을 학습시키는 도구.
- TensorBoard: 학습 그래프를 보는 도구.

해야 할 일:

- 위 프로그램들이 설치되는지 확인한다.
- `scripts/check_runtime.py`를 실행해서 import가 되는지 확인한다.
- Windows에서 너무 느리거나 영상 문제가 있으면 WSL2 Ubuntu 환경을 준비한다.

WSL2를 쓸 때 할 일:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip ffmpeg
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
python3 scripts/check_runtime.py
```

이 단계가 끝났다는 기준:

- 시뮬레이션 관련 프로그램들이 에러 없이 불러와진다.
- 나중에 영상을 만들기 위한 `ffmpeg`도 준비된다.

## 2단계: 첫 번째 로봇 미션 만들기

목표: 가장 쉬운 문제부터 만든다.

첫 번째 미션:

- 물건은 1개만 나온다.
- 박스도 1개만 있다.
- 로봇은 물건을 집어서 박스에 넣으면 된다.

왜 이렇게 시작하는가:

- 처음부터 여러 물건과 여러 박스를 쓰면 실패 원인을 찾기 어렵다.
- 먼저 "집기와 놓기"가 되는지 확인해야 한다.
- 이 단계가 되어야 다음 분류 문제로 넘어갈 수 있다.

해야 할 일:

- 로봇 손 위치, 물건 위치, 박스 위치가 상태값에 들어가는지 확인한다.
- 로봇 행동이 `앞뒤`, `좌우`, `위아래`, `집게 열기/닫기`로 동작하는지 확인한다.
- 물건이 목표 박스 근처에 가면 성공으로 처리되는지 확인한다.

이 단계가 끝났다는 기준:

- 테스트에서 첫 번째 미션 환경이 정상 생성된다.
- 성공/실패 판정이 코드에서 확인된다.

## 3단계: 첫 번째 모델 짧게 학습시키기

목표: 모델 성능이 아니라 학습 과정이 돌아가는지 확인한다.

쉽게 말하면:

- 로봇에게 아주 짧게 연습을 시킨다.
- 이 단계에서는 잘하는 로봇을 기대하지 않는다.
- "학습 프로그램이 실행되는가", "모델 파일이 저장되는가"만 확인한다.

실행할 명령:

```powershell
.\.venv\Scripts\python.exe scripts\train.py --stage 1 --algo sac --total-timesteps 1000 --output-dir checkpoints\smoke --tensorboard-log runs\smoke
```

명령의 뜻:

- `--stage 1`: 첫 번째 쉬운 미션을 학습한다.
- `--algo sac`: SAC라는 강화학습 방법을 쓴다.
- `--total-timesteps 1000`: 아주 짧게 1000번만 연습한다.
- `--output-dir checkpoints\smoke`: 모델 파일을 저장할 폴더다.
- `--tensorboard-log runs\smoke`: 학습 기록을 저장할 폴더다.

이 단계가 끝났다는 기준:

- `checkpoints/smoke/stage1_sac.zip` 모델 파일이 생긴다.
- `runs/smoke` 폴더에 학습 로그가 생긴다.

## 4단계: 저장된 모델 로드하기

목표: 저장한 모델 파일을 다시 불러와서 평가할 수 있는지 확인한다.

왜 중요한가:

- 모델을 저장만 하고 다시 못 불러오면 결과물을 쓸 수 없다.
- 포트폴리오에서는 "학습했다"보다 "저장한 모델을 다시 실행해 확인했다"가 더 중요하다.

실행할 명령:

```powershell
.\.venv\Scripts\python.exe scripts\evaluate.py --stage 1 --checkpoint checkpoints\smoke\stage1_sac.zip --episodes 5
```

명령의 뜻:

- `--stage 1`: 첫 번째 미션으로 시험한다.
- `--checkpoint`: 불러올 모델 파일 위치다.
- `--episodes 5`: 5번 시험해 본다.

확인할 결과:

- 성공률이 출력되는가.
- 평균 보상이 출력되는가.
- 모델 파일을 못 찾는 에러가 없는가.
- 저장한 모델과 평가 환경이 서로 맞는가.

주의:

- 1000번만 학습한 smoke 모델은 성공률이 낮아도 정상이다.
- 이 단계는 성능 검증이 아니라 "저장과 로드 검증"이다.

## 5단계: 두 번째 로봇 미션 만들기

목표: 단순히 넣는 것을 넘어서 "분류"를 하게 만든다.

두 번째 미션:

- 물건 종류가 여러 개 있다.
- 박스가 3개 있다.
- 로봇은 물건 종류를 보고 맞는 박스에 넣어야 한다.

예시:

- 빨간 물건은 1번 박스.
- 파란 물건은 2번 박스.
- 초록 물건은 3번 박스.

해야 할 일:

- 물건 종류 정보가 로봇 상태에 들어가는지 확인한다.
- 물건 종류에 따라 목표 박스가 달라지는지 확인한다.
- 잘못된 박스에 넣었을 때 성공으로 처리되지 않는지 확인한다.

이 단계가 끝났다는 기준:

- Stage 2 환경 테스트가 통과한다.
- 물건 종류와 목표 박스 매칭이 코드에서 확인된다.

## 6단계: 더 오래 학습하고 성공률 확인하기

목표: 실제로 쓸 만한 모델이 되는지 확인한다.

해야 할 일:

- Stage 1을 더 오래 학습한다.
- 저장된 모델을 100번 정도 평가한다.
- 성공률과 평균 보상을 기록한다.
- Stage 1이 어느 정도 안정되면 Stage 2도 학습한다.

실행 예시:

```bash
python3 scripts/train.py --stage 1 --algo sac --total-timesteps 50000 --seed 42 --output-dir checkpoints/stage1 --tensorboard-log runs/stage1
python3 scripts/evaluate.py --stage 1 --checkpoint checkpoints/stage1/stage1_sac.zip --episodes 100
```

Stage 2 예시:

```bash
python3 scripts/train.py --stage 2 --algo sac --total-timesteps 50000 --seed 42 --output-dir checkpoints/stage2 --tensorboard-log runs/stage2
python3 scripts/evaluate.py --stage 2 --checkpoint checkpoints/stage2/stage2_sac.zip --episodes 100
```

기록해야 할 것:

- 몇 번 학습했는가.
- 어떤 모델 파일이 생겼는가.
- 성공률이 얼마인가.
- 평균 보상이 얼마인가.
- 실패했다면 어떤 상황에서 실패했는가.

주의:

- 성공률을 측정하지 않았으면 성공했다고 쓰면 안 된다.
- 한 번의 결과만 보고 "항상 잘된다"고 쓰면 안 된다.

## 7단계: 결과 영상과 그래프 만들기

목표: 결과를 눈으로 보여줄 수 있게 만든다.

해야 할 일:

- 학습 전 모델 또는 초기 상태 영상을 만든다.
- 중간 학습 모델 영상을 만든다.
- 최종 학습 모델 영상을 만든다.
- TensorBoard 그래프를 캡처한다.
- README와 Notion 기록에 명령, 모델 경로, 성공률을 같이 적는다.

영상 생성 예시:

```bash
python3 scripts/record_video.py --stage 1 --checkpoint checkpoints/stage1/stage1_sac.zip --output videos/stage1_rollout.mp4
python3 scripts/record_video.py --stage 2 --checkpoint checkpoints/stage2/stage2_sac.zip --output videos/stage2_rollout.mp4
```

포트폴리오에 넣을 자료:

- 프로젝트 한 줄 설명.
- 환경설정 과정.
- 첫 번째 미션과 두 번째 미션 설명.
- 학습 명령.
- 모델 파일 경로.
- 평가 결과.
- 영상.
- 실패했던 문제와 해결 방법.

## 8단계: 고도화

목표: 기본 프로젝트가 된 뒤 기술적으로 더 깊게 만든다.

나중에 할 수 있는 일:

- SAC 말고 TD3 같은 다른 강화학습 방법과 비교한다.
- 더 실제 같은 MuJoCo 로봇 환경으로 바꾼다.
- 물건 개수를 늘린다.
- 카메라 이미지 기반 인식으로 확장한다.
- Docker로 실행 환경을 묶는다.

주의:

- 고도화는 기본 모델 저장/로드/평가가 된 뒤에 한다.
- 처음부터 고도화를 하면 실패 원인을 찾기 어렵다.

## 지금 당장 우선순위

1. Python과 `.venv` 복구.
2. 필요한 시뮬레이션 프로그램 설치 확인.
3. Stage 1 환경 실행 확인.
4. Stage 1 짧은 학습 실행.
5. 모델 파일 저장 확인.
6. 저장한 모델 로드 평가.
7. Stage 2 분류 환경 확인.
8. 긴 학습과 영상 제작.

## 각 단계가 끝날 때 기록할 것

매번 아래 항목을 남긴다.

- 실행한 명령.
- 성공했는지 실패했는지.
- 실패했다면 에러 메시지.
- 생성된 모델 파일 경로.
- 생성된 로그 폴더 경로.
- 평가 성공률.
- 평균 보상.
- 영상 파일 경로.

기록 예시:

```text
단계: Stage 1 짧은 학습
명령: python scripts/train.py --stage 1 --algo sac --total-timesteps 1000
결과: checkpoint 생성됨
모델 파일: checkpoints/smoke/stage1_sac.zip
로그 폴더: runs/smoke
검증 상태: 모델 로드는 아직 확인 전
```

## 최종 목표

최종적으로는 다음 문장을 증거와 함께 말할 수 있어야 한다.

"가상 로봇 분류 환경을 만들고, 강화학습으로 로봇을 훈련시켰으며, 저장된 모델을 다시 불러와 평가하고, 결과 영상과 수치로 검증했다."
