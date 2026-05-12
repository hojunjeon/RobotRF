# 분리수거 로봇팔 강화학습 프로젝트 기획서

## 1. 프로젝트 개요

### 목표
- **1순위**: 로보틱스 SW 개발자 포트폴리오 제작 -> 노션 블로그 작성
- **2순위**: 강화학습 및 로봇팔 실습 경험 습득

### 한 줄 요약
MuJoCo 시뮬레이터에서 로봇팔이 물체를 종류에 따라 올바른 분리수거 박스에 넣는 법을 강화학습으로 단계적으로 학습하는 시스템

---

## 2. 타겟 직군 및 포트폴리오 전략

### 타겟 직군
- 로보틱스 SW 개발자 (현대차, 현대로보틱스 등)
- AI/ML 엔지니어링

### 포트폴리오 스토리
> "MuJoCo에서 로봇팔 환경을 직접 구성하고, SAC + HER 알고리즘으로 물체 분류 태스크를 Curriculum Learning 방식으로 단계적으로 학습시켰다"

### 어필 포인트
- 환경 설계 + 제어 + AI 세 가지를 한 프로젝트에서 시연
- Curriculum Learning으로 학습 과정의 개선이 눈에 보임
- Claude Code를 활용한 AI 툴 기반 개발 경험
- W&B 학습 곡선 + 시연 영상으로 임팩트 시각화

---

## 3. 기술 스택

| 역할 | 툴 |
|---|---|
| 물리 시뮬레이터 | MuJoCo |
| 환경 API | Gymnasium / Gymnasium-Robotics |
| RL 알고리즘 | SAC + HER (Stable-Baselines3) |
| 학습 모니터링 | W&B / TensorBoard |
| 영상 녹화 | VecVideoRecorder + ffmpeg |
| 개발 보조 | Claude Code |
| 배포/정리 | Docker Compose (선택) |

---

## 4. 강화학습 구성

### 알고리즘: SAC + HER
- **SAC** (Soft Actor-Critic): 로봇팔 연속 행동 공간에 최적화된 표준 알고리즘
- **HER** (Hindsight Experience Replay): 초반 실패 경험을 재활용해 희소 보상 환경에서 학습 효율 극대화

### 환경 구성 요소

| 요소 | 내용 |
|---|---|
| 상태 (State) | 관절 각도, 엔드이펙터 위치, 물체 위치/종류, 박스 위치 |
| 행동 (Action) | 관절 토크값, 그리퍼 열기/닫기 |
| 보상 (Reward) | 집기 성공 +1, 올바른 박스 +10, 잘못된 박스 -5, 낙하 -1 |
| 종료 조건 | 박스에 넣으면 성공 / 스텝 초과 시 실패 |

---

## 5. Curriculum Learning 단계 설계

### 1단계 — Pick & Place 기초
- 물체 1개를 로봇팔 앞에 생성
- 로봇팔이 집어서 박스 1개에 넣기
- **목표**: 집고 내려놓는 기본 동작 학습

### 2단계 — 분류 학습
- 3가지 종류의 물체와 박스 3개 준비
- 물체를 1개씩 생성하여 올바른 박스에 분류
- **목표**: 물체 인식 + 분류 판단 학습

### 3단계 — 대량 분류
- 3가지 물체를 대량으로 동시 생성
- 우선순위를 스스로 결정하며 분류
- **목표**: 복잡한 환경에서의 효율적 처리 학습

> **참고**: 2주 일정상 1~2단계 완성 + 3단계는 향후 계획으로 구성

---

## 6. 개발 환경

### 로컬 사양
- CPU: Intel i7-11700 (8코어 / 16스레드)
- RAM: 32GB
- GPU: NVIDIA RTX 5060 Ti 16GB
- OS: Windows 11 + WSL2 (Ubuntu 22.04)

### 환경 구성
```
Windows
└── WSL2 (Ubuntu 22.04)
    ├── CUDA 12.8
    ├── PyTorch 2.6 (GPU)
    ├── MuJoCo
    ├── Gymnasium-Robotics
    └── Stable-Baselines3
```

### 예상 학습 속도 (RTX 5060 Ti 기준)
- 50,000 스텝: 약 10~20분
- 200,000 스텝: 약 1시간 내외

---

## 7. 개발 로드맵 (2주)

| 기간 | 작업 |
|---|---|
| 1~3일 | WSL2 환경 세팅 + MuJoCo + 오픈소스 로봇팔 import |
| 4~6일 | 1단계 환경 구성 + SAC+HER 학습 |
| 7~10일 | 2단계 분류 환경 구성 + 학습 |
| 11~14일 | 체크포인트 영상 편집 + README + W&B 정리 |

---

## 8. 포트폴리오 산출물

### 필수
- 학습 곡선 그래프 (W&B / TensorBoard)
- 체크포인트별 시연 영상 (Before / Middle / After)
- GitHub README (시스템 아키텍처 다이어그램 포함)

### 선택
- Docker Compose 원클릭 실행 환경
- 알고리즘 비교 실험 (SAC vs PPO 성능 그래프)

---

## 9. 참고 레퍼런스

- [Multi-Robot Arm Sorting with RL (arxiv 2024)](https://arxiv.org/abs/2409.13511)
- [MuJoCo + Franka Pick & Place 오픈소스 환경 (arxiv)](https://arxiv.org/pdf/2312.13788)
- [SAC Pick & Place 93.2% 성공률 논문](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10296071/)

---

## 10. 향후 확장 계획

- 3단계 대량 분류 구현
- 컨베이어 벨트 환경으로 확장
- 비전 기반 물체 인식 모듈 추가 (카메라 센서)
- 실제 로봇팔 하드웨어 이전 (Sim2Real)
