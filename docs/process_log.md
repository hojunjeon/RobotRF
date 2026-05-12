# Process Log

이 파일은 Notion 블로그 초안 작성 전 단계의 작업 기록이다. 모든 내용을 그대로 글로 옮기기보다, 의미 있는 결정과 증거만 선별해 글로 확장한다.

## 2026-05-13 KST

### 프로젝트 스펙 확정

- 2주 MVP 범위는 테이블탑 시뮬레이션에서 Stage 1 Pick & Place와 Stage 2 단일 물체 분류로 고정했다.
- 실행 환경은 WSL2 Ubuntu 22.04 네이티브로 정했다.
- Docker는 MVP 필수가 아니라 재현성 강화용 후순위 산출물로 뺐다.
- RL 학습은 SAC + HER를 메인으로 두고, TD3/TQC/DDPG/PPO/DQN 계열은 확장 후보로 문서화하기로 했다.

블로그 후보:

- 프로젝트 기획편
- MVP 범위 설정과 제외한 것들

### 초기 구현

- GoalEnv-compatible 테이블탑 환경을 추가했다.
- 학습/평가/영상 녹화 CLI를 추가했다.
- WSL2 Quickstart와 HTML 아키텍처 다이어그램을 추가했다.
- 현재 Windows 환경에는 Python과 WSL 배포판이 없어 테스트와 학습 smoke test는 실행하지 못했다.

블로그 후보:

- 시뮬레이션 설계편
- 실행 환경 구축편

### GitHub 연동

- 로컬 폴더를 Git 저장소로 초기화했다.
- remote를 `https://github.com/hojunjeon/RobotRF.git`로 설정했다.
- remote가 빈 저장소임을 `git ls-remote origin`으로 확인했다.
- 5개 단위 commit을 만들고 `origin/main`으로 push했다.

커밋:

- `a932c2f chore: initialize robot sorting rl project`
- `0625564 feat: add tabletop sorting goal environment`
- `b5a77f3 feat: add sac her training and evaluation scripts`
- `4d4e182 test: add goal env and algorithm registry tests`
- `65f7c2e docs: add wsl2 quickstart and portfolio materials`

블로그 후보:

- GitHub 프로젝트 초기화와 작업 단위 commit 전략
