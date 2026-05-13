# Recording Handoff Log

이 파일은 개발 에이전트가 기록 담당 에이전트에게 넘기는 append-only 작업 로그다.
최종 Notion 글은 이 로그를 바탕으로 별도 에이전트가 작성한다.

## 001 - 2026-05-13 KST - 기록 인계 규칙 추가

### 오늘 한 일
- 개발 에이전트와 기록 에이전트의 역할을 분리하는 프로젝트 규칙을 `AGENTS.md`에 추가했다.
- 기록 담당 에이전트가 읽을 표준 프로토콜을 `docs/recording_handoff_protocol.md`로 추가했다.
- 앞으로 개발 작업 후 기록용 정보를 누적할 append-only 로그 파일을 만들었다.

### 막힌 문제
- 기존 `docs/process_log.md`, `docs/notion_blog_strategy.md`, `docs/notion_blog_template.md` 일부가 현재 PowerShell 출력에서 인코딩이 깨져 보인다.

### 해결 방법 / 결정
- 기존 문서를 즉시 대체하지 않고, UTF-8 한국어로 된 새 인계 문서를 추가했다.
- 개발 에이전트는 최종 블로그 글을 쓰지 않고, 기록 담당 에이전트가 바로 가져갈 수 있는 사실/증거 패킷만 남기도록 규칙을 명시했다.

### 남은 문제
- 기존 Notion 전략/템플릿 문서의 실제 인코딩을 확인하고 필요하면 UTF-8로 정리해야 한다.
- 향후 학습/평가/영상 생성 작업이 발생하면 이 로그에 결과 지표와 산출물 경로를 계속 추가해야 한다.

### 증거
- 코드 경로:
  - `AGENTS.md`
  - `docs/recording_handoff_protocol.md`
  - `docs/recording_handoff_log.md`
- 실행 명령:
  - `git remote -v`
  - `git log --oneline -5`
  - `Get-Content -LiteralPath 'C:\Users\SSAFY\Desktop\RRF\pyproject.toml'`
  - `Get-Content -LiteralPath 'C:\Users\SSAFY\Desktop\RRF\README.md' -TotalCount 180`
- 결과 로그/지표:
  - 원격 저장소: `https://github.com/hojunjeon/RobotRF.git`
  - 패키지 이름: `robot-sorting-rl`
  - 최근 커밋 예시: `bfbfc11 docs: add notion blog workflow`
- 스크린샷/영상:
  - 없음
- 체크포인트/학습 로그:
  - 없음
- 커밋:
  - 아직 미커밋

### 기록 담당 에이전트에게 강조할 관점
- 채용 담당자: 개발과 기록을 역할 분리하여 프로젝트 운영 체계를 만들었다.
- 기술 면접관: 산출물 주장과 실제 검증 증거를 분리하는 evidence-first 규칙을 추가했다.
- 개발자/학습자: 이후 작업자는 같은 템플릿으로 명령, 로그, 실패 원인을 재현 가능하게 남길 수 있다.

### 검증 상태
- 검증 완료:
  - `AGENTS.md`, `README.md`, `pyproject.toml`, git remote, 최근 커밋 정보를 로컬에서 확인했다.
- 검증 불가:
  - 기록 담당 에이전트의 실제 Notion 작성 플로우는 이 세션에서 실행하지 않았다.
- 가정:
  - 프로젝트 최종 포트폴리오 톤은 사용자가 준 요구를 바탕으로 채용 포트폴리오형 + 기술 블로그형 + Notion 공개 페이지형으로 둔다.
---

## 002 - 2026-05-13 KST - Windows 실행 환경 부트스트랩 진단

### 오늘 한 일
- 현재 폴더에서 바로 테스트/학습을 시작하려고 로컬 Python, WSL, `.venv` 상태를 확인했다.
- `.venv`가 존재하지만 실행 가능한 Python 환경이 아니라는 문제를 재현했다.
- WSL Ubuntu 22.04 설치를 시도했지만 배포판 등록이 완료되지 않아 학습 실행 전 단계에서 막혔다.
- 같은 막힘을 재현 가능하게 만들기 위해 `scripts/check_windows_bootstrap.ps1`를 추가했다.
- 부트스트랩 스크립트를 검증하는 `tests/check_bootstrap_script.ps1`를 추가했다.
- README의 WSL2 Quickstart 앞에 Windows bootstrap check 명령을 추가했다.

### 막힌 문제
- `.\.venv\Scripts\python.exe -m pytest` 실행 시 Python 프로세스 생성에 실패했다.
- `python --version`은 명령을 찾지 못했다.
- `py --version`은 `No installed Python found!`를 반환했다.
- `wsl --list --all --verbose`는 등록된 Linux 배포판이 없다는 메시지를 반환했다.
- `wsl --install -d Ubuntu-22.04`와 `wsl --install Ubuntu-22.04 --name RRF-Ubuntu-22.04 --web-download`는 제한 시간 안에 완료되지 않았다.

### 해결 방법 / 결정
- 현재 세션에서 학습 smoke test를 억지로 진행하지 않고, 실행 환경 문제를 먼저 명시적으로 진단하는 스크립트를 추가했다.
- 스크립트는 Python, WSL, `.venv`, `.venv\Scripts\python.exe` 실행 가능 여부를 출력하고 문제가 있으면 종료 코드 1을 반환한다.
- PowerShell 테스트는 스크립트가 필수 섹션을 출력하고 종료 코드가 0 또는 1인지 확인한다.

### 남은 문제
- WSL2 Ubuntu 22.04 배포판을 정상 등록해야 한다.
- Ubuntu 내부에서 `python3 -m venv .venv`, `make install`, `python3 scripts/check_runtime.py`, `make test`를 실행해야 한다.
- 테스트가 통과하면 Stage 1 학습 smoke test와 TensorBoard/W&B 로그 생성을 진행해야 한다.

### 증거
- 코드 경로:
  - `scripts/check_windows_bootstrap.ps1`
  - `tests/check_bootstrap_script.ps1`
  - `README.md`
  - `docs/recording_handoff_log.md`
- 실행 명령:
  - `.\.venv\Scripts\python.exe -m pytest`
  - `python --version`
  - `py --version`
  - `wsl --status`
  - `wsl --list --all --verbose`
  - `wsl --install -d Ubuntu-22.04`
  - `wsl --install Ubuntu-22.04 --name RRF-Ubuntu-22.04 --web-download`
  - `powershell -NoProfile -ExecutionPolicy Bypass -File .\tests\check_bootstrap_script.ps1`
  - `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_windows_bootstrap.ps1`
- 결과 로그/지표:
  - `.venv\Scripts\python.exe -m pytest`: `Unable to create process`
  - `python --version`: command not found
  - `py --version`: `No installed Python found!`
  - bootstrap test: exit code 0
  - bootstrap check: exit code 1, Python/WSL/.venv python 문제 출력
- 스크린샷/영상:
  - 없음
- 체크포인트/학습 로그:
  - 없음
- 커밋:
  - 아직 미커밋

### 기록 담당 에이전트에게 강조할 관점
- 채용 담당자: 학습 실행 전 환경 리스크를 자동 진단 가능한 산출물로 바꿨다.
- 기술 면접관: 실패를 숨기지 않고 Python/WSL/venv 계층을 분리해 root cause를 좁혔다.
- 개발자/학습자: Windows에서 시작할 때 가장 먼저 실행할 수 있는 재현 명령과 다음 조치를 README에 연결했다.

### 검증 상태
- 검증 완료:
  - `tests/check_bootstrap_script.ps1`가 실패하는 RED 상태를 먼저 확인했다.
  - `scripts/check_windows_bootstrap.ps1` 구현 후 `tests/check_bootstrap_script.ps1`가 exit code 0으로 통과했다.
  - `scripts/check_windows_bootstrap.ps1`가 현재 환경 문제를 exit code 1로 출력하는 것을 확인했다.
- 검증 불가:
  - Python/WSL 배포판이 아직 정상 등록되지 않아 `make test`, `scripts/check_runtime.py`, 학습 smoke test는 실행하지 못했다.
- 가정:
  - 현재 Windows 세션에서 학습을 직접 돌리기보다 WSL2 Ubuntu 환경을 정상화한 뒤 실행하는 것이 프로젝트 README의 의도와 맞다.
---

## 003 - 2026-05-13 KST - Windows 로컬 실행 환경 완료

### 오늘 한 일
- WSL 설치/apt 경로가 오래 걸리는 병목이 되어 Windows `.venv` 경로로 전환했다.
- `C:\Users\SSAFY\AppData\Local\Python\pythoncore-3.14-64\python.exe`로 프로젝트 `.venv`를 재생성했다.
- Python 3.14에서 wheel이 있는 조합으로 `gymnasium`, `gymnasium-robotics`, `mujoco` 의존성 제약을 조정했다.
- `scripts/check_runtime.py`의 Fetch 환경을 deprecated된 `FetchPickAndPlace-v3`에서 `FetchPickAndPlace-v4`로 변경했다.
- Stable-Baselines3 progress bar extra 의존성 없이 smoke training이 가능하도록 `train_sac(progress_bar=False)` 기본값을 추가했다.
- Windows Quickstart를 README에 추가하고 WSL은 장기 학습 선택지로 정리했다.
- Stage 1 학습 smoke test를 실행해 checkpoint와 TensorBoard 로그를 생성했다.

### 막힌 문제
- WSL Ubuntu 내부에서 `.venv-wsl` 생성 시 `ensurepip`가 없어 `python3.10-venv` 설치가 필요했다.
- `sudo apt-get update && sudo apt-get install ...` 경로는 시간이 오래 걸려 중단하고 Windows `.venv` 경로로 전환했다.
- 기존 `pyproject.toml`의 `gymnasium<1.1` 제약 때문에 pip가 `gymnasium-robotics==1.3.1`, `mujoco==3.1.6` 소스 빌드로 내려가며 `MUJOCO_PATH` 오류가 발생했다.
- `scripts/check_runtime.py`는 최신 Gymnasium-Robotics에서 deprecated된 `FetchPickAndPlace-v3`를 사용해 실패했다.
- 학습 smoke test는 `progress_bar=True` 때문에 `tqdm`, `rich` extra 의존성을 요구하며 실패했다.

### 해결 방법 / 결정
- Windows 로컬 `.venv`를 현재 검증 가능한 기본 경로로 채택했다.
- 의존성 제약을 `gymnasium>=1.2,<1.4`, `gymnasium-robotics>=1.4.2,<2.0`, `mujoco>=3.8.1,<4.0`로 변경했다.
- Fetch runtime check는 `FetchPickAndPlace-v4`를 사용하도록 수정했다.
- 학습 함수는 progress bar를 기본 비활성화해 최소 설치 환경에서 smoke test가 돌도록 수정했다.
- WSL은 배포판 등록 상태만 확인하고, 장기 학습용 선택지로 남겼다.

### 남은 문제
- 장기 학습을 WSL-native 경로에서 돌리려면 Ubuntu 내부에 `python3.10-venv`, `python3-pip`, `ffmpeg` 설치가 추가로 필요하다.
- smoke test 성공률은 0.0으로, 학습 성능 검증이 아니라 실행 경로 검증으로만 해석해야 한다.
- 다음 개발 단계는 Stage 1 reward/환경 동작 점검과 baseline 학습 시간 확장이다.

### 증거
- 코드 경로:
  - `pyproject.toml`
  - `scripts/check_runtime.py`
  - `src/robot_sorting_rl/training.py`
  - `tests/test_check_runtime_script.py`
  - `tests/test_training_defaults.py`
  - `README.md`
  - `.gitignore`
- 실행 명령:
  - `.\.venv\Scripts\python.exe -m pip install -e .[dev]`
  - `.\.venv\Scripts\python.exe scripts\check_runtime.py`
  - `.\.venv\Scripts\python.exe -m pytest`
  - `.\.venv\Scripts\python.exe scripts\train.py --stage 1 --algo sac --total-timesteps 1000 --output-dir checkpoints\smoke --tensorboard-log runs\smoke`
  - `.\.venv\Scripts\python.exe scripts\evaluate.py --stage 1 --checkpoint checkpoints\smoke\stage1_sac.zip --episodes 5`
  - `.\.venv\Scripts\python.exe -m pip check`
  - `.\.venv\Scripts\python.exe -m ruff check .`
  - `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_windows_bootstrap.ps1`
- 결과 로그/지표:
  - bootstrap check: exit code 0, `.venv python status: RUNNABLE`, Python 3.14.2
  - runtime check: torch 2.11.0+cpu, cuda false, mujoco 3.8.1, render shape `(480, 480, 3)`
  - pytest: 8 passed
  - pip check: `No broken requirements found.`
  - ruff: `All checks passed!`
  - smoke train: 1000 timesteps 완료, `checkpoints\smoke\stage1_sac.zip` 저장
  - smoke evaluate: 5 episodes, success_rate 0.0, mean_reward -50.0, mean_episode_length 50.0
- 스크린샷/영상:
  - 없음
- 체크포인트/학습 로그:
  - `checkpoints\smoke\stage1_sac.zip`
  - `runs\smoke\SAC_1`
  - `runs\smoke\SAC_2`
- 커밋:
  - 아직 미커밋

### 기록 담당 에이전트에게 강조할 관점
- 채용 담당자: 환경 설정 병목을 WSL 고집 없이 Windows `.venv` 우회로 해결해 실행 가능한 기준선을 확보했다.
- 기술 면접관: 패키지 resolver가 구버전 MuJoCo 소스 빌드로 내려간 원인을 의존성 제약으로 특정하고 wheel 기반 조합으로 수정했다.
- 개발자/학습자: bootstrap check, runtime check, pytest, smoke train, smoke evaluate까지 재현 명령을 남겼다.

### 검증 상태
- 검증 완료:
  - Windows `.venv` 생성과 의존성 설치
  - MuJoCo/Gymnasium-Robotics runtime import/render
  - 전체 테스트 8개 통과
  - Stage 1 SAC+HER smoke training checkpoint 생성
  - checkpoint load/evaluate 경로 확인
  - pip dependency consistency와 ruff check
- 검증 불가:
  - WSL Ubuntu 내부 패키지 설치는 시간 병목으로 완료하지 않았다.
  - 장기 학습 성공률 목표는 아직 검증하지 않았다.
- 가정:
  - 현재 단계의 목표는 성능 달성이 아니라 재현 가능한 로컬 실행 환경 확보와 smoke test 통과다.
---

## 004 - 2026-05-13 KST - 토큰 절약 프로젝트 스킬 추가

### 오늘 한 일
- RTK, Caveman, Context Mode, Code Review Graph 등 여러 토큰 절약 아이디어를 검토했다.
- 여러 아이디어를 하나로 묶은 프로젝트 로컬 스킬 `skills/token-economy/SKILL.md`를 추가했다.
- 세부 비교와 에이전트 포팅 메모를 `skills/token-economy/references/` 아래에 분리했다.
- 다른 에이전트가 작업 전에 참고할 수 있도록 `AGENTS.md`에 Token Economy Policy를 추가했다.

### 막힌 문제
- 당시 Windows 로컬에서 `python`, `py -3`, `.venv\Scripts\python.exe` 실행이 불안정해 `skill-creator`의 `init_skill.py`와 `quick_validate.py`를 정상 실행하지 못했다.

### 해결 방법 / 결정
- Python 런타임 문제가 해결되기 전까지 수동으로 스킬 표준 구조를 작성했다.
- 개별 아이디어를 여러 스킬로 쪼개기보다, 저장소 탐색/로그 압축/리뷰 범위 제한/증거 보존을 하나의 `token-economy` 스킬로 통합했다.
- 세부 설명은 reference 파일로 분리해 기본 로딩 비용을 낮췄다.

### 남은 문제
- 당시에는 Codex 전역 스킬 경로(`$CODEX_HOME/skills`)에 설치하지 않았고, 프로젝트 내부 스킬로만 추가했다.
- 외부 에이전트 런타임별 자동 탐지 여부는 검증하지 못했다.

### 증거
- 코드 경로:
  - `AGENTS.md`
  - `skills/token-economy/SKILL.md`
  - `skills/token-economy/references/repo-comparison.md`
  - `skills/token-economy/references/agent-portability.md`
  - `skills/token-economy/agents/openai.yaml`
- 실행 명령:
  - `python C:\Users\SSAFY\.codex\skills\.system\skill-creator\scripts\init_skill.py token-economy --path skills --resources references ...`
  - `.\.venv\Scripts\python.exe C:\Users\SSAFY\.codex\skills\.system\skill-creator\scripts\init_skill.py token-economy --path skills --resources references ...`
  - `py -3 C:\Users\SSAFY\.codex\skills\.system\skill-creator\scripts\init_skill.py token-economy --path skills --resources references ...`
  - `New-Item -ItemType Directory -Force skills\token-economy\references, skills\token-economy\agents`
  - `Get-Content -Raw skills\token-economy\SKILL.md`
  - `git diff -- AGENTS.md skills/token-economy/SKILL.md skills/token-economy/references/repo-comparison.md skills/token-economy/references/agent-portability.md skills/token-economy/agents/openai.yaml`
  - PowerShell frontmatter check for `skills\token-economy\SKILL.md`
- 결과 로그/지표:
  - `SKILL.md` frontmatter check: `frontmatter ok`
  - `python`: command not found
  - `py -3`: `No installed Python found!`
  - `.venv\Scripts\python.exe`: process creation failure
- 스크린샷/영상:
  - 없음
- 체크포인트/학습 로그:
  - 없음
- 커밋:
  - 아직 미커밋

### 기록 담당 에이전트에게 강조할 관점
- 채용 담당자: 여러 AI 에이전트가 같은 작업 원칙을 따르도록 프로젝트 내부 운영 스킬을 만들었다.
- 기술 면접관: 단순한 문서 추가가 아니라 컨텍스트 절약, 증거 보존, 리뷰 범위 제한을 하나의 운영 정책으로 구조화했다.
- 개발자/학습자: 에이전트 자동화가 없어도 `rg`, 제한된 파일 읽기, 실패 중심 로그 요약, blast-radius 기반 리뷰를 적용할 수 있다.

### 검증 상태
- 검증 완료:
  - `SKILL.md` frontmatter 수동 확인
  - 관련 파일 생성 확인
  - `git diff`로 `AGENTS.md` 반영 확인
- 검증 불가:
  - `skill-creator` 공식 `quick_validate.py` 실행은 당시 Python 런타임 문제로 불가
- 가정:
  - 프로젝트 내부 `skills/token-economy/`를 다른 에이전트가 읽거나, 각 플랫폼 지침 파일에서 연결하면 동일한 원칙을 적용할 수 있다.
---

## 005 - 2026-05-13 KST - 토큰 절약 스킬 간이 사용량 테스트

### 오늘 한 일
- `token-economy` 스킬 적용 전/후의 컨텍스트 수집량을 같은 작업 기준으로 비교했다.
- 작업 기준: 토큰 절약 스킬 추가 변경사항을 리뷰하기 위한 컨텍스트 수집.

### 막힌 문제
- 실제 모델/API 토큰 카운터는 사용할 수 없었다.

### 해결 방법 / 결정
- 로컬 텍스트 길이를 기준으로 `ceil(characters / 4)` 추정 토큰을 계산했다.
- 미적용 조건은 관련 파일 본문과 diff를 그대로 포함했다.
- 적용 조건은 `git status`, `git diff --stat`, 헤딩, 핵심 비교 라인, 플랫폼별 섹션 라인만 포함했다.

### 남은 문제
- 실제 에이전트별 토크나이저와 한국어/영어 혼합 문서에서는 절대 토큰 수가 달라질 수 있다.

### 증거
- 실행 명령:
  - PowerShell에서 raw context와 compact context를 구성하고 문자 수, 단어 수, `ceil(characters / 4)` 추정 토큰을 계산
- 결과 로그/지표:
  - 미적용 raw context: 13,155 characters, 1,891 words, 3,289 estimated tokens
  - 적용 compact context: 2,775 characters, 295 words, 694 estimated tokens
  - 추정 토큰 감소율: 78.9%
- 코드 경로:
  - `skills/token-economy/SKILL.md`
  - `skills/token-economy/references/repo-comparison.md`
  - `skills/token-economy/references/agent-portability.md`
  - `AGENTS.md`
- 커밋:
  - 아직 미커밋

### 기록 담당 에이전트에게 강조할 관점
- 채용 담당자: 간단한 실험에서 컨텍스트 수집량을 약 79% 줄이는 운영 효과를 수치로 확인했다.
- 기술 면접관: 동일 작업 기준으로 raw 파일/diff 읽기와 선택적 요약 읽기를 비교했으며, 절대 토큰은 추정치임을 분리했다.
- 개발자 학습: 실제 API 토큰 카운터가 없어도 문자 수 기반 근사로 정책 효과를 빠르게 검증할 수 있다.

### 검증 상태
- 검증 완료:
  - PowerShell 계산 출력 확인
- 검증 불가:
  - 실제 모델별 tokenizer/API usage 값 측정
- 가정:
  - `ceil(characters / 4)`는 영어 중심 코드/Markdown 컨텍스트의 간이 토큰 추정치로만 사용한다.
---

## 006 - 2026-05-13 KST - 토큰 절약 스킬 기본 ON 정책 반영

### 오늘 한 일
- `token-economy` 스킬 운영 방식을 `default ON + 특정 상황에서만 OFF/relax`로 명시했다.
- `AGENTS.md`의 Token Economy Policy도 같은 기본값으로 수정했다.
- `agents/openai.yaml` 기본 프롬프트를 default ON 정책에 맞게 갱신했다.

### 막힌 문제
- 공식 `quick_validate.py`는 `py -3` 실행 시 `No installed Python found!`로 실행할 수 없었다.

### 해결 방법 / 결정
- PowerShell 기반으로 `SKILL.md` frontmatter와 주요 문구를 검증했다.
- OFF/relax 예외는 상세 교육, 블로그/README/포트폴리오 문장, 브레인스토밍, 원문 로그/전문 요청, 고위험 분석으로 제한했다.

### 남은 문제
- 실제 전역 Codex skill registry 검증은 Python 런타임 부재로 수행하지 못했다.

### 증거
- 코드 경로:
  - `skills/token-economy/SKILL.md`
  - `skills/token-economy/agents/openai.yaml`
  - `AGENTS.md`
- 실행 명령:
  - `Select-String -Path skills\token-economy\SKILL.md -Pattern '^Default to ON','^## Default Mode','Keep token economy ON','Turn it OFF','If unsure' -Context 0,8`
  - `Select-String -Path AGENTS.md -Pattern '^## Token Economy Policy','Default ON','Turn it OFF' -Context 0,7`
  - PowerShell frontmatter check for `skills\token-economy\SKILL.md`
  - `py -3 C:\Users\SSAFY\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\token-economy`
- 결과 로그/지표:
  - `frontmatter ok`
  - `quick_validate.py`: `No installed Python found!`
- 커밋:
  - 아직 미커밋

### 검증 상태
- 검증 완료:
  - default ON 섹션 반영 확인
  - `AGENTS.md` 정책 반영 확인
  - `agents/openai.yaml` 기본 프롬프트 확인
  - `SKILL.md` frontmatter 확인
- 검증 불가:
  - 공식 skill quick validation
---

## 007 - 2026-05-13 KST - 프로젝트 로컬 스킬 라우팅 정리

### 오늘 한 일
- clone된 저장소 안에서 바로 참조할 수 있도록 `skills/rrf-project-ops`와 `skills/rrf-recording-handoff`를 추가했다.
- 기존 `skills/token-economy`의 description을 `Use when...` 형식으로 조정했다.
- `AGENTS.md`를 짧은 라우터로 줄이고 상세 운영 규칙은 프로젝트 로컬 스킬로 이동했다.
- 프로젝트 스킬 구조를 검증하는 `tests/test_project_skills.py`를 추가했다.
- 스킬 validator 실행을 위해 `pyyaml`을 dev 의존성에 추가했다.

### 막힌 문제
- `quick_validate.py`가 `PyYAML`을 요구했지만 dev 의존성에 없어 `ModuleNotFoundError: No module named 'yaml'`로 실패했다.
- `rrf-recording-handoff`에 UTF-8 한글 템플릿이 들어가자 Windows 기본 CP949 읽기에서 `UnicodeDecodeError`가 발생했다.
- `docs/recording_handoff_log.md`에 인코딩이 섞인 구간이 있어 일반 패치 도구가 바로 수정하지 못했다.

### 해결 방법 / 결정
- `pyyaml>=6.0`을 dev 의존성에 추가했다.
- `AGENTS.md`는 스킬 경로와 기본 원칙만 남겨 clone 후 라우팅 비용을 줄였다.
- 자동 탐지가 안 되는 에이전트도 `AGENTS.md`의 로컬 스킬 경로를 직접 열면 작업 규칙을 따를 수 있게 했다.

### 남은 문제
- 외부 에이전트 런타임별 자동 스킬 탐지는 이 세션에서 검증하지 않았다.

### 증거
- 코드 경로: `AGENTS.md`, `skills/rrf-project-ops/SKILL.md`, `skills/rrf-recording-handoff/SKILL.md`, `skills/token-economy/SKILL.md`, `tests/test_project_skills.py`, `pyproject.toml`
- 실행 명령: `init_skill.py`로 두 스킬 생성, `pytest tests/test_project_skills.py`, `quick_validate.py`로 세 스킬 검증
- 결과 로그/지표: 프로젝트 스킬 테스트 통과, 세 로컬 스킬 `Skill is valid!`
- 스크린샷/영상: 없음
- 체크포인트/학습 로그: 없음
- 커밋: 아직 미커밋

### 기록 담당 에이전트에게 강조할 관점
- 채용 담당자: 프로젝트 운영 규칙을 clone 가능한 로컬 스킬로 제품화해 협업 재현성을 높였다.
- 기술 면접관: `AGENTS.md`를 얇은 라우팅 계층으로 유지하고 세부 정책을 버전 관리되는 스킬로 분리했다.
- 개발자/학습자: 새 에이전트는 로컬 스킬 경로만 읽어도 작업 방식과 기록 방식을 따라갈 수 있다.

### 검증 상태
- 검증 완료: 스킬 템플릿 생성, 프로젝트 스킬 테스트 통과, 세 개 스킬의 quick validator 통과
- 검증 불가: 외부 에이전트 런타임별 자동 스킬 탐지
- 가정: clone 후 최소 호환 경로는 `AGENTS.md`가 지시하는 로컬 `skills/*/SKILL.md`를 직접 읽는 방식이다.
---

## 008 - 2026-05-13 KST - 기록 인계 순번 규칙 적용

### 오늘 한 일
- `docs/recording_handoff_log.md`의 모든 최상위 기록 항목에 3자리 순번을 붙였다.
- `skills/rrf-recording-handoff/SKILL.md`와 `docs/recording_handoff_protocol.md`에 `NNN - YYYY-MM-DD KST - 제목` 형식을 명시했다.
- 기록 항목 순번을 강제하는 테스트를 추가했다.

### 막힌 문제
- 같은 날짜에 여러 기록이 있어 제목만으로는 특정 기록을 지칭하기 어려웠다.

### 해결 방법 / 결정
- `001`부터 시작하는 3자리 순번을 사용한다.
- 새 항목은 기존 최대 번호에 1을 더해 append-only로 추가한다.

### 남은 문제
- 없음

### 증거
- 코드 경로: `docs/recording_handoff_log.md`, `docs/recording_handoff_protocol.md`, `skills/rrf-recording-handoff/SKILL.md`, `tests/test_project_skills.py`
- 실행 명령: `pytest tests/test_project_skills.py`, `quick_validate.py skills/rrf-recording-handoff`
- 결과 로그/지표: 기록 순번 테스트 통과, 기록 인계 스킬 validator 통과
- 스크린샷/영상: 없음
- 체크포인트/학습 로그: 없음
- 커밋: 아직 미커밋

### 기록 담당 에이전트에게 강조할 관점
- 채용 담당자: 작업 이력이 안정적인 번호로 식별 가능해졌다.
- 기술 면접관: 환경 설정은 `003`, 스킬 라우팅은 `007`처럼 근거를 번호로 참조할 수 있다.
- 개발자/학습자: 긴 제목을 복사하지 않고도 기록을 빠르게 인용할 수 있다.

### 검증 상태
- 검증 완료: 순번 테스트 통과, 기록 인계 스킬 validator 통과
- 검증 불가: 없음
- 가정: 기록 번호는 재사용하지 않고 append-only로 유지한다.
---

## 009 - 2026-05-13 KST - 기존 기록명 정리

### 오늘 한 일
- 기존 기록 제목을 읽을 수 있는 한국어 제목으로 정리했다.
- 깨져 있던 `004` 제목을 `토큰 절약 프로젝트 스킬 추가`로 수정했다.
- 영문 제목이던 `007`, `008`을 한국어 제목으로 바꿨다.
- 기록 제목에 손상 문자가 들어오면 실패하는 테스트를 추가했다.

### 막힌 문제
- 이전 인코딩 문제 때문에 일부 제목이 깨져 보였다.
- 일부 제목이 영어로 남아 기록명 스타일이 일관되지 않았다.

### 해결 방법 / 결정
- 모든 최상위 기록 제목을 `NNN - YYYY-MM-DD KST - 한국어 제목` 형식으로 맞췄다.
- 기록 제목 가독성을 테스트로 관리한다.

### 남은 문제
- 당시에는 제목 중심으로 정리했고, 본문 전체 품질 검사는 아직 충분하지 않았다.

### 증거
- 코드 경로: `docs/recording_handoff_log.md`, `tests/test_project_skills.py`
- 실행 명령: `pytest tests/test_project_skills.py`
- 결과 로그/지표: 제목 가독성 테스트 통과
- 스크린샷/영상: 없음
- 체크포인트/학습 로그: 없음
- 커밋: 아직 미커밋

### 기록 담당 에이전트에게 강조할 관점
- 채용 담당자: 작업 로그가 읽을 수 있는 번호형 마일스톤으로 정리됐다.
- 기술 면접관: 기존 증거를 `003`, `007`처럼 안정적으로 참조할 수 있다.
- 개발자/학습자: 기록명이 일관되어 빠르게 스캔할 수 있다.

### 검증 상태
- 검증 완료: 제목 순번 및 손상 문자 방지 테스트 통과
- 검증 불가: 당시 본문 전체 손상 여부는 완전히 검사하지 못했다.
- 가정: 이 단계에서는 사용자가 기록명 수정을 요청했다.
---

## 010 - 2026-05-13 KST - 004번 기록과 한글 기록 기준 복구

### 오늘 한 일
- 004번 기록의 깨진 한글 본문을 읽을 수 있는 한국어 문장으로 복구했다.
- 007~009번 기록의 영문 섹션명과 영문 본문을 한국어 기록 형식으로 정리했다.
- `rrf-recording-handoff` 스킬의 기록 템플릿을 한글 기본 형식으로 수정했다.
- 기록 로그 본문에 replacement-character나 mojibake marker가 남으면 실패하는 테스트를 추가했다.
- 기록 로그의 섹션명이 한국어 표준 목록을 벗어나면 실패하는 테스트를 추가했다.

### 막힌 문제
- 이전 검증은 제목만 검사해서 004번 본문 손상과 007~009번 영문 섹션을 놓쳤다.
- 한글 스킬 파일은 Windows 기본 인코딩 validator에서 바로 읽히지 않아 UTF-8 모드 검증이 필요했다.

### 해결 방법 / 결정
- 기록 로그 전체 본문을 검사하는 테스트로 범위를 넓혔다.
- 기록 섹션명은 `오늘 한 일`, `막힌 문제`, `해결 방법 / 결정`, `남은 문제`, `증거`, `기록 담당 에이전트에게 강조할 관점`, `검증 상태`만 허용한다.
- 사용자가 직접 지시하지 않아도 간단한 인코딩/표기 오류는 개발 에이전트가 먼저 잡는 기준으로 고정했다.

### 남은 문제
- 없음

### 증거
- 코드 경로: `docs/recording_handoff_log.md`, `skills/rrf-recording-handoff/SKILL.md`, `tests/test_project_skills.py`
- 실행 명령: `pytest tests/test_project_skills.py`, `quick_validate.py skills/rrf-recording-handoff` with `PYTHONUTF8=1`
- 결과 로그/지표: 기록 품질 테스트 통과 예정
- 스크린샷/영상: 없음
- 체크포인트/학습 로그: 없음
- 커밋: 아직 미커밋

### 기록 담당 에이전트에게 강조할 관점
- 채용 담당자: 기록 품질을 자동 검증 대상으로 끌어올렸다.
- 기술 면접관: 제목뿐 아니라 본문 인코딩 손상과 섹션 언어까지 테스트로 방지한다.
- 개발자/학습자: 프로젝트 기록은 번호, 한국어 제목, 한국어 섹션명, 읽을 수 있는 본문을 유지해야 한다.

### 검증 상태
- 검증 완료: 예정
- 검증 불가: 없음
- 가정: 간단한 기록 품질 오류는 개발 에이전트가 선제적으로 수정해야 한다.
---

## 011 - 2026-05-13 KST - 비전공자용 프로젝트 로드맵 문서 추가

### 오늘 한 일
- 환경설정, 강화학습 시뮬레이션 프로그램 설치, 첫 미션 구성, 모델 학습, 모델 저장, 모델 로드, 평가, 영상 정리 순서로 로드맵을 다시 작성했다.
- 기존 개발자용 표현인 GoalEnv, HER, checkpoint, TensorBoard 같은 용어는 쉬운 설명을 먼저 붙이고 필요한 곳에서만 사용했다.
- 사용자가 비전공자 기준으로 이해하기 어렵다고 지적한 부분을 반영해 `docs/project_roadmap.md`를 전면 재작성했다.

### 막힌 문제
- 현재 로컬 Python 실행 환경은 이전 push 작업에서 pytest 실행이 불가능한 상태로 확인되었다.

### 해결 방법 / 결정
- 새 로드맵은 비전공자가 따라갈 수 있도록 "무엇을 설치하는지", "무엇을 실행하는지", "어떤 파일이 생기는지" 중심으로 구성했다.
- Stage 1은 물건 1개를 박스 1개에 넣는 미션, Stage 2는 물건 종류에 따라 3개 박스 중 맞는 곳에 넣는 미션으로 설명했다.
- 성능 검증과 단순 실행 확인을 구분하도록 "짧은 학습은 모델 품질 검증이 아니다"라는 주의 문구를 남겼다.

### 남은 문제
- 로컬 `.venv` 복구 후 `scripts/check_runtime.py`와 `pytest`를 다시 실행해야 한다.
- 실제 학습 결과가 나오면 성공률, 평균 보상, 모델 파일, 영상 파일 경로를 문서에 추가해야 한다.

### 증거
- 코드 경로: `docs/project_roadmap.md`, `docs/recording_handoff_log.md`
- 실행 명령: 문서 작성 작업이라 테스트 명령은 아직 실행하지 않음
- 결과 로그/지표: 비전공자용 로드맵 문서로 재작성
- 스크린샷/영상: 없음
- 체크포인트/학습 로그: 없음
- 커밋: 아직 미커밋

### 기록 담당 에이전트에게 강조할 관점
- 채용 담당자: 비전공자도 프로젝트 진행 순서를 이해할 수 있도록 환경설정부터 모델 로드까지 흐름을 풀어 썼다.
- 기술 면접관: 어려운 용어를 숨기지 않고, 먼저 쉬운 개념으로 설명한 뒤 실제 명령과 연결했다.
- 개발자/학습자: 지금 당장 해야 할 일이 Python 복구, 시뮬레이션 설치 확인, Stage 1 짧은 학습, 모델 로드 검증 순서로 정리됐다.

### 검증 상태
- 검증 완료: 문서 파일 생성 및 기록 append
- 검증 불가: 로컬 Python 환경 문제로 pytest 재실행은 아직 불가
- 가정: 로드맵은 현재 README와 스크립트 기준의 계획 문서이며, 실제 학습 성능을 증명하지 않는다.
---

## 012 - 2026-05-13 KST - 로드맵 2단계 실행 절차 보강

### 오늘 한 일
- `docs/project_roadmap.md`의 "2단계: 첫 번째 로봇 미션 만들기"에 실제 구현 파일, 테스트 파일, 확인 명령, Stage 1 환경 생성 명령을 추가했다.
- 기존 설명이 "무엇을 해야 하는지" 수준에 머물러 있어, 사용자가 바로 따라할 수 있는 PowerShell 명령과 확인 기준으로 보강했다.
- Stage 1이 `TabletopSortingEnv(stage=1)`로 구성되고, `training.py`의 `make_env(stage=1)`을 통해 학습 스크립트와 연결된다는 점을 문서화했다.

### 막힌 문제
- `.venv`의 Python 실행 파일이 `"/usr/bin\python.exe"`를 가리키는 깨진 상태라 pytest와 Python 한 줄 환경 생성 검증은 실행되지 않았다.

### 해결 방법 / 결정
- 2단계는 새 기능 구현이 아니라 이미 존재하는 Stage 1 환경을 사용자가 검증할 수 있게 만드는 문서 보강으로 처리했다.
- 성공 판정은 `success_threshold`, `is_success`, `compute_reward` 확인으로 안내했다.
- 테스트는 `tests/test_tabletop_sorting_env.py`를 직접 실행하는 방식으로 안내했다.

### 남은 문제
- 로컬 `.venv` 복구 후 `.\.venv\Scripts\python.exe -m pytest tests\test_tabletop_sorting_env.py`를 다시 실행해야 한다.
- 로컬 `.venv` 복구 후 Stage 1 환경 생성 한 줄 명령도 다시 실행해야 한다.

### 증거
- 코드 경로: `docs/project_roadmap.md`, `src/robot_sorting_rl/envs/tabletop_sorting.py`, `src/robot_sorting_rl/training.py`, `tests/test_tabletop_sorting_env.py`
- 실행 명령:
  - `Select-String -Path .\src\robot_sorting_rl\envs\tabletop_sorting.py -Pattern "target_index = 0 if self.stage == 1 else self.object_type"`
  - `Select-String -Path .\src\robot_sorting_rl\envs\tabletop_sorting.py -Pattern "self.gripper_position|self.object_position|self.desired_goal"`
  - `Select-String -Path .\src\robot_sorting_rl\envs\tabletop_sorting.py -Pattern "success_threshold|is_success|compute_reward"`
  - `.\.venv\Scripts\python.exe -m pytest tests\test_tabletop_sorting_env.py`
  - `.\.venv\Scripts\python.exe -c "from robot_sorting_rl.envs import TabletopSortingEnv; env=TabletopSortingEnv(stage=1); obs,info=env.reset(seed=7); print(obs.keys()); print(info)"`
- 결과 로그/지표:
  - `target_index = 0 if self.stage == 1 else self.object_type` 확인됨
  - `gripper_position`, `object_position`, `desired_goal` 확인됨
  - `success_threshold`, `is_success`, `compute_reward` 확인됨
  - pytest/Python 실행 실패: `No Python at '"/usr/bin\python.exe'`
- 스크린샷/영상: 없음
- 체크포인트/학습 로그: 없음
- 커밋: 아직 미커밋

### 기록 담당 에이전트에게 강조할 관점
- 채용 담당자: 비전공자도 첫 로봇 미션을 코드 위치와 명령으로 추적할 수 있게 정리했다.
- 기술 면접관: Stage 1 환경 계약, GoalEnv 관찰값, 성공 판정, 테스트 기준을 명확히 연결했다.
- 개발자/학습자: 막연한 "미션 만들기"를 `TabletopSortingEnv(stage=1)` 생성과 pytest 검증으로 바꾸었다.

### 검증 상태
- 검증 완료: 문서 변경 diff 확인, Stage 1 코드 위치/상태값/성공 판정 검색 명령 확인
- 검증 불가: `.venv` Python 경로 문제로 pytest와 Python 환경 생성 명령 실행 불가
- 가정: 이 작업은 문서 보강이며, 학습 성능 수치를 새로 주장하지 않는다.
---

## 013 - 2026-05-13 KST - 초보자 자급형 로드맵 재작성

### 오늘 한 일
- 사용자가 Codex 외 도구를 모른다는 전제를 반영해 `docs/project_roadmap.md`를 초보자 실행서 형태로 전면 재작성했다.
- MuJoCo, Gymnasium/Gymnasium-Robotics, SAC+HER, TensorBoard, W&B, 영상 녹화, Codex, Docker Compose의 역할을 "처음 보는 사람 기준 설명", "이 프로젝트에서 쓰는 위치", "필수 여부"로 나눠 정리했다.
- 각 단계마다 목표, 실행 명령, 정상 기준, 막혔을 때 판단 기준, 기록해야 할 증거를 추가했다.
- 현재 저장소의 실제 구현과 다른 부분은 과장하지 않고 분리했다. 기본 영상 녹화는 `scripts/record_video.py`와 `imageio`이며, `VecVideoRecorder`는 선택 고도화로 명시했다.
- W&B는 `pyproject.toml`의 선택 의존성에는 있으나 기본 학습 스크립트에 직접 연결되어 있지 않으므로 선택 고도화로 명시했다.

### 막힌 문제
- 로컬 `.venv`가 이전과 같이 `No Python at '"/usr/bin\python.exe'` 상태일 가능성이 있어 Python 기반 검증은 아직 제한된다.

### 해결 방법 / 결정
- 로드맵의 기본 경로는 현재 코드가 실제 지원하는 Windows PowerShell 명령으로 작성했다.
- 성능 검증과 실행 경로 검증을 분리했다. 1000 timestep smoke 학습은 실행 확인으로만 설명했다.
- W&B, Docker Compose, VecVideoRecorder는 처음부터 요구하지 않고 기본 학습/평가/영상 저장 이후 붙이는 고도화 항목으로 뺐다.

### 남은 문제
- `.venv` 복구 후 로드맵의 Python 명령을 0단계부터 순서대로 재검증해야 한다.
- Docker Compose와 VecVideoRecorder를 실제 기본 기능으로 쓰려면 별도 코드/설정 작업이 필요하다.
- W&B를 기본 모니터링으로 쓰려면 학습 스크립트에 W&B 초기화와 로그 연결을 추가해야 한다.

### 증거
- 코드 경로: `docs/project_roadmap.md`, `docs/recording_handoff_log.md`, `pyproject.toml`, `scripts/train.py`, `scripts/evaluate.py`, `scripts/record_video.py`, `src/robot_sorting_rl/training.py`
- 실행 명령:
  - `Get-Content -Path .\pyproject.toml -Encoding UTF8`
  - `Get-Content -Path .\scripts\train.py -Encoding UTF8`
  - `Get-Content -Path .\scripts\evaluate.py -Encoding UTF8`
  - `Get-Content -Path .\scripts\record_video.py -Encoding UTF8`
- 결과 로그/지표:
  - `pyproject.toml`에서 `wandb`는 선택 의존성으로 확인
  - `scripts/record_video.py`가 `imageio.v2`를 사용함을 확인
  - `scripts/train.py`가 `--stage`, `--algo sac`, `--total-timesteps`, `--seed`, `--output-dir`, `--tensorboard-log` 옵션을 제공함을 확인
  - `scripts/evaluate.py`가 JSON metrics를 출력함을 확인
- 스크린샷/영상: 없음
- 체크포인트/학습 로그: 없음
- 커밋: 아직 미커밋

### 기록 담당 에이전트에게 강조할 관점
- 채용 담당자: 사용자가 모르는 도구 묶음을 자급형 실행 로드맵으로 바꿔 프로젝트 운영 가능성을 높였다.
- 기술 면접관: 실제 저장소가 지원하는 기본 경로와 선택 고도화를 분리해 과장 없이 기술 범위를 정리했다.
- 개발자/학습자: 이제 로드맵은 개념 설명이 아니라 복붙 가능한 명령, 성공 기준, 막힘 판단표를 포함한다.

### 검증 상태
- 검증 완료: 실제 스크립트와 `pyproject.toml`을 읽고 로드맵 도구 설명을 맞춤
- 검증 불가: `.venv` 복구 전 Python 실행 명령 재검증 불가
- 가정: 이 작업은 문서 재작성이며, 새 학습 성능이나 새 체크포인트를 주장하지 않는다.
---

## 014 - 2026-05-13 KST - WSL Python 명령 혼동 수정

### 오늘 한 일
- 사용자가 WSL Ubuntu 프롬프트에서 Windows PowerShell용 `.\.venv\Scripts\python.exe -m pytest`를 실행해 `command not found`와 `No Python at '"/usr/bin\python.exe'` 오류를 만난 사례를 반영했다.
- `docs/project_roadmap.md` 앞부분에 "내가 쓰는 터미널 고르기" 섹션을 추가했다.
- Windows PowerShell과 WSL Ubuntu의 Python 명령 형태, 경로 구분자, TensorBoard 실행 명령 차이를 표로 정리했다.
- WSL에서 깨진 `.venv`를 `deactivate`, `rm -rf .venv`, `python3 -m venv .venv`, `source .venv/bin/activate` 순서로 복구하는 절차를 추가했다.

### 막힌 문제
- 사용자가 현재 WSL에서 실행 중이므로 Windows용 `.venv\Scripts\python.exe` 명령은 동작하지 않는다.
- 기존 `.venv`는 Windows/WSL 경로가 섞인 상태로 보이며 `No Python at '"/usr/bin\python.exe'`를 출력했다.

### 해결 방법 / 결정
- WSL에서는 가상환경 활성화 후 `python -m pytest`처럼 Linux 방식 명령만 쓰도록 문서화했다.
- Windows 명령과 WSL 명령을 섞지 않는 것을 최상단 원칙으로 추가했다.
- 이후 문서에 Windows 명령이 나오더라도 WSL 사용자는 변환표를 보고 `.\.venv\Scripts\python.exe`를 `python`으로 바꾸도록 안내했다.

### 남은 문제
- 사용자가 WSL에서 `.venv`를 재생성한 뒤 `python scripts/check_runtime.py`와 `python -m pytest` 결과를 확인해야 한다.

### 증거
- 코드 경로: `docs/project_roadmap.md`, `docs/recording_handoff_log.md`
- 실행 명령:
  - 사용자 실행: `.\.venv\Scripts\python.exe -m pytest`
  - 사용자 실행: `.venv/Scripts/python.exe -m pytest`
  - 권장 WSL 실행: `python -m pytest`
- 결과 로그/지표:
  - `..venvScriptspython.exe: command not found`
  - `.venvScriptspython.exe: command not found`
  - `No Python at '"/usr/bin\python.exe'`
- 스크린샷/영상: 없음
- 체크포인트/학습 로그: 없음
- 커밋: 아직 미커밋

### 기록 담당 에이전트에게 강조할 관점
- 채용 담당자: 초보자가 터미널 환경 차이 때문에 막히지 않도록 실행 로드맵의 현실성을 높였다.
- 기술 면접관: 오류 원인을 코드가 아니라 Windows/WSL 가상환경 경로 혼용으로 정확히 분리했다.
- 개발자/학습자: WSL에서는 `.venv/bin/python` 계열을 쓰고 Windows에서는 `.venv\Scripts\python.exe` 계열을 쓴다는 기준을 명확히 했다.

### 검증 상태
- 검증 완료: 사용자 오류 로그를 원인별로 분류하고 문서에 WSL 복구 절차 반영
- 검증 불가: 실제 WSL 터미널에서 `.venv` 재생성과 pytest 재실행은 사용자 환경에서 필요
- 가정: 사용자는 이후 WSL Ubuntu에서 계속 진행한다.
---

## 015 - 2026-05-13 KST - AGENTS 라우터 길이 테스트 복구

### 오늘 한 일
- WSL에서 `python -m pytest` 실행 결과 `tests/test_project_skills.py::test_agents_md_is_short_skill_router`가 실패한 원인을 확인했다.
- 실패 원인은 `AGENTS.md`가 41줄로 늘어나 테스트 기준인 35줄 이하를 넘긴 것이었다.
- `AGENTS.md`에서 상세 coding behavior 섹션을 제거하고, 프로젝트 로컬 스킬로 상세 규칙을 위임하는 짧은 라우터 형태로 되돌렸다.

### 막힌 문제
- Windows 쪽에서 `wsl -d Ubuntu`는 배포판 이름 불일치로 실패했다.

### 해결 방법 / 결정
- 기본 WSL 호출인 `wsl -- bash -lc "..."`로 사용자가 실행한 것과 같은 Linux Python 환경에서 테스트했다.
- `AGENTS.md`는 상세 규칙을 담지 않고 `skills/rrf-project-ops`, `skills/token-economy`, `skills/rrf-recording-handoff`로 라우팅하는 역할만 유지한다.

### 남은 문제
- 없음

### 증거
- 코드 경로: `AGENTS.md`, `tests/test_project_skills.py`, `docs/recording_handoff_log.md`
- 실행 명령:
  - `wsl -- bash -lc "cd /mnt/c/Users/user/Desktop/RobotRF && source .venv/bin/activate && python -m pytest tests/test_project_skills.py::test_agents_md_is_short_skill_router"`
  - `wsl -- bash -lc "cd /mnt/c/Users/user/Desktop/RobotRF && source .venv/bin/activate && python -m pytest"`
- 결과 로그/지표:
  - 단일 테스트: `1 passed in 0.10s`
  - 전체 테스트: `15 passed in 1.66s`
- 스크린샷/영상: 없음
- 체크포인트/학습 로그: 없음
- 커밋: 아직 미커밋

### 기록 담당 에이전트에게 강조할 관점
- 채용 담당자: 사용자가 직접 WSL 환경을 복구하고 전체 테스트 실행까지 도달했다.
- 기술 면접관: 실패 원인을 환경 문제가 아니라 AGENTS 라우터 길이 계약 위반으로 분리했고, 최소 수정으로 복구했다.
- 개발자/학습자: 테스트 실패 메시지의 `41 <= 35`를 읽고 파일 책임을 줄이는 방식으로 해결했다.

### 검증 상태
- 검증 완료: WSL 환경에서 실패 단일 테스트와 전체 pytest 통과
- 검증 불가: 없음
- 가정: `AGENTS.md`의 상세 행동 규칙은 프로젝트 스킬 문서에서 관리한다.
---

## 016 - 2026-05-13 KST - AGENTS 실행 규칙 보존과 테스트 계약 수정

### 오늘 한 일
- 사용자 피드백에 따라 `AGENTS.md`가 단순 라우터가 아니라 실행 규칙을 포함하는 운영 문서임을 재확인했다.
- 이전에 제거했던 `AGENTS.md`의 coding behavior 섹션을 복구했다.
- `tests/test_project_skills.py`의 `len(text.splitlines()) <= 35` 검증을 제거했다.
- 테스트 이름을 `test_agents_md_routes_to_skills_and_keeps_operating_rules`로 바꾸고, 필수 스킬 라우팅과 `Coding Behavior`, `Think Before Coding`, `Simplicity First`, `Surgical Changes`, `Goal-Driven Execution` 존재를 검증하게 수정했다.

### 막힌 문제
- 이전 판단은 `AGENTS.md`를 짧은 라우터로만 해석해 실행 규칙을 삭제하는 방향으로 잘못 수정했다.

### 해결 방법 / 결정
- 소스 문서인 `AGENTS.md`의 실행 규칙을 보존하고, 테스트가 현재 문서 책임을 검증하도록 바꿨다.
- 길이 제한은 현재 운영 정책과 맞지 않으므로 제거했다.

### 남은 문제
- 없음

### 증거
- 코드 경로: `AGENTS.md`, `tests/test_project_skills.py`, `docs/recording_handoff_log.md`
- 실행 명령:
  - `wsl -- bash -lc "cd /mnt/c/Users/user/Desktop/RobotRF && source .venv/bin/activate && python -m pytest tests/test_project_skills.py::test_agents_md_routes_to_skills_and_keeps_operating_rules -q"`
- 결과 로그/지표:
  - 단일 테스트: `1 passed in 0.11s`
- 스크린샷/영상: 없음
- 체크포인트/학습 로그: 없음
- 커밋: 아직 미커밋

### 기록 담당 에이전트에게 강조할 관점
- 채용 담당자: 사용자의 운영 기준 피드백을 반영해 테스트 계약을 실제 프로젝트 운영 방식에 맞췄다.
- 기술 면접관: 문서 책임을 잘못 줄이는 대신, 테스트가 문서의 필수 라우팅과 실행 규칙을 검증하도록 수정했다.
- 개발자/학습자: 실패한 테스트를 무조건 만족시키는 것이 아니라 테스트의 가정이 맞는지 검토해야 한다.

### 검증 상태
- 검증 완료: 수정된 단일 테스트 통과
- 검증 불가: 전체 테스트는 이 기록 추가 후 재실행 필요
- 가정: `AGENTS.md`는 라우팅과 항상 적용할 실행 규칙을 함께 담는 문서다.
---

## 017 - 2026-05-13 KST - Stage 1 초보자 설명 보강

### 오늘 한 일
- 사용자가 "3단계: Stage 1 첫 번째 로봇 미션 확인"이 비전공자에게 이해되지 않는다고 지적한 내용을 반영했다.
- `docs/project_roadmap.md`의 Stage 1 섹션을 게임판 비유로 다시 작성했다.
- 로봇 손, 물건, 목표 박스, 성공 거리, 행동 4개 숫자, 관찰값 13개, 성공/실패 보상 구조를 표와 쉬운 문장으로 설명했다.
- WSL Ubuntu와 Windows PowerShell 명령을 나눠 Stage 1 환경 생성, 코드 확인, 테스트 실행 절차를 추가했다.
- 이 단계의 핵심 문장을 "로봇 손, 물건, 목표 박스가 있는 작은 책상 게임판을 만들고, 물건이 목표 박스에 가까워지면 성공이라고 판정하는지 확인하는 단계"로 정리했다.

### 막힌 문제
- 일부 WSL 확인 명령은 Codex 쪽 PowerShell에서 WSL로 넘기는 quoting 문제 때문에 재현 검증이 실패했다.
- Stage 1 테스트 명령은 WSL에서 정상 통과했다.

### 해결 방법 / 결정
- 초보자에게 필요한 것은 코드 조각보다 상황 이해이므로, Stage 1을 먼저 "게임판/캐릭터/아이템/목적지"로 설명했다.
- 학습 실행 전 환경 이해와 테스트 확인을 분리했다.

### 남은 문제
- 사용자가 실제 WSL 터미널에서 문서의 `python -c ...` 출력 확인 명령을 직접 실행해 화면 출력이 이해되는지 확인해야 한다.

### 증거
- 코드 경로: `docs/project_roadmap.md`, `docs/recording_handoff_log.md`, `src/robot_sorting_rl/envs/tabletop_sorting.py`, `tests/test_tabletop_sorting_env.py`
- 실행 명령:
  - `wsl -- bash -lc "cd /mnt/c/Users/user/Desktop/RobotRF && source .venv/bin/activate && python -m pytest tests/test_tabletop_sorting_env.py::test_stage1_reset_returns_goal_env_observation tests/test_tabletop_sorting_env.py::test_step_reports_success_when_object_reaches_desired_goal -q"`
- 결과 로그/지표:
  - Stage 1 관련 테스트: `2 passed in 1.50s`
- 스크린샷/영상: 없음
- 체크포인트/학습 로그: 없음
- 커밋: 아직 미커밋

### 기록 담당 에이전트에게 강조할 관점
- 채용 담당자: 비전공자가 프로젝트를 따라갈 수 있도록 로봇 강화학습 환경을 게임판 비유로 설명했다.
- 기술 면접관: Stage 1의 관찰값, 행동 공간, 보상, 성공 판정이 코드와 연결되도록 문서화했다.
- 개발자/학습자: "테스트를 실행한다" 전에 "무슨 상황을 테스트하는지"를 이해하도록 순서를 바꿨다.

### 검증 상태
- 검증 완료: Stage 1 관련 pytest 2개 통과
- 검증 불가: Codex PowerShell→WSL quoting 문제로 일부 한 줄 출력 명령은 도구에서 직접 검증하지 못함
- 가정: 사용자는 WSL Ubuntu에서 직접 명령을 실행한다.
---

## 018 - 2026-05-13 KST - Stage 1 시각화 스냅샷 추가

### 오늘 한 일
- 사용자가 Stage 1 설명을 눈으로 볼 수 있는지 물어본 것을 반영해 환경 스냅샷 생성 기능을 추가했다.
- `scripts/render_snapshot.py`를 추가해 `python scripts/render_snapshot.py --stage 1 --output docs/stage1_snapshot.png` 명령으로 Stage 1 이미지를 저장할 수 있게 했다.
- `tests/test_render_snapshot_script.py`를 추가해 스냅샷 스크립트가 PNG 파일을 생성하는지 검증했다.
- `docs/project_roadmap.md`의 Stage 1 섹션에 "먼저 눈으로 보기" 절차와 `docs/stage1_snapshot.png` 이미지를 추가했다.

### 막힌 문제
- 없음

### 해결 방법 / 결정
- 초보자에게 한 줄 Python 명령보다 전용 스크립트가 더 따라 하기 쉬우므로 별도 CLI 스크립트로 만들었다.
- 기존 `TabletopSortingEnv.render()`와 `imageio`를 재사용했다.

### 남은 문제
- 없음

### 증거
- 코드 경로: `scripts/render_snapshot.py`, `tests/test_render_snapshot_script.py`, `docs/project_roadmap.md`, `docs/stage1_snapshot.png`
- 실행 명령:
  - `wsl -- bash -lc "cd /mnt/c/Users/user/Desktop/RobotRF && source .venv/bin/activate && python -m pytest tests/test_render_snapshot_script.py -q"`
  - `wsl -- bash -lc "cd /mnt/c/Users/user/Desktop/RobotRF && source .venv/bin/activate && python scripts/render_snapshot.py --stage 1 --output docs/stage1_snapshot.png"`
- 결과 로그/지표:
  - 스냅샷 테스트: `1 passed in 2.26s`
  - 스냅샷 생성: `saved snapshot: docs/stage1_snapshot.png`
  - 생성 파일 크기: `2093` bytes
- 스크린샷/영상: `docs/stage1_snapshot.png`
- 체크포인트/학습 로그: 없음
- 커밋: 아직 미커밋

### 기록 담당 에이전트에게 강조할 관점
- 채용 담당자: 추상적인 강화학습 환경을 실제 이미지로 보여줘 비전공자 이해 장벽을 낮췄다.
- 기술 면접관: 기존 환경의 `render()` 계약을 재사용해 시각화 스냅샷 CLI와 테스트를 추가했다.
- 개발자/학습자: Stage 1을 숫자 관찰값 전에 이미지로 먼저 확인하는 흐름으로 바꿨다.

### 검증 상태
- 검증 완료: 스냅샷 스크립트 테스트 통과, Stage 1 이미지 생성 확인
- 검증 불가: 없음
- 가정: Stage 1 스냅샷은 환경 이해용이며 학습 성능 증거가 아니다.
---

## 019 - 2026-05-13 KST - 로봇팔 모델 확인 단계와 Fetch 스냅샷 추가

### 오늘 한 일
- 사용자가 기대한 "시뮬레이션 툴 실행, 로봇팔 모델 로드, 실제 움직임 확인"이 현재 로드맵에서 어디에 해당하는지 정리했다.
- 현재 저장소에는 Franka/Panda 모델 파일이 없고, 즉시 확인 가능한 로봇팔 예제는 Gymnasium-Robotics의 `FetchPickAndPlace-v4`임을 문서화했다.
- `scripts/render_robotics_env.py`를 추가해 `FetchPickAndPlace-v4` 로봇팔 장면을 PNG로 저장할 수 있게 했다.
- `tests/test_render_robotics_env_script.py`를 추가해 Gymnasium-Robotics 렌더 스크립트가 PNG 파일을 생성하는지 검증했다.
- `docs/project_roadmap.md`에 "MuJoCo 로봇팔 모델 화면 확인" 단계를 추가하고, Franka/Panda는 별도 고도화 통합 항목으로 분리했다.

### 막힌 문제
- 처음 Windows `Get-Item` 확인은 파일을 못 찾았지만, WSL `ls`와 이후 Windows `Get-ChildItem`에서 `docs/fetch_pick_and_place_snapshot.png` 생성이 확인되었다.

### 해결 방법 / 결정
- 현재 가능한 로봇팔 확인은 Fetch로 수행한다.
- Franka/Panda는 현재 저장소에 없는 모델이므로 "이미 확인 가능"하다고 쓰지 않고, 별도 asset 추가와 Gymnasium 환경 구현이 필요한 고도화로 정리했다.

### 남은 문제
- 실제 Franka/Panda 로봇팔을 쓰려면 MuJoCo XML/MJCF asset 추가와 전용 환경 구현이 필요하다.
- "움직임 확인"까지 가려면 정지 이미지 다음 단계로 action을 몇 step 넣어 GIF/MP4를 생성하는 스크립트를 추가해야 한다.

### 증거
- 코드 경로: `scripts/render_robotics_env.py`, `tests/test_render_robotics_env_script.py`, `docs/project_roadmap.md`, `docs/fetch_pick_and_place_snapshot.png`
- 실행 명령:
  - `wsl -- bash -lc "cd /mnt/c/Users/user/Desktop/RobotRF && source .venv/bin/activate && python -m pytest tests/test_render_robotics_env_script.py -q"`
  - `wsl -- bash -lc "cd /mnt/c/Users/user/Desktop/RobotRF && source .venv/bin/activate && python scripts/render_robotics_env.py --env-id FetchPickAndPlace-v4 --output docs/fetch_pick_and_place_snapshot.png"`
  - `wsl -- bash -lc "cd /mnt/c/Users/user/Desktop/RobotRF && source .venv/bin/activate && python -m pytest"`
- 결과 로그/지표:
  - 로봇팔 스냅샷 테스트: `1 passed in 4.03s`
  - 스냅샷 생성: `saved snapshot: docs/fetch_pick_and_place_snapshot.png`
  - 생성 파일: `PNG image data, 480 x 480`
  - 전체 테스트: `17 passed in 6.96s`
- 스크린샷/영상: `docs/fetch_pick_and_place_snapshot.png`
- 체크포인트/학습 로그: 없음
- 커밋: 아직 미커밋

### 기록 담당 에이전트에게 강조할 관점
- 채용 담당자: 사용자의 원래 기대와 현재 MVP 사이의 차이를 숨기지 않고 로드맵에 반영했다.
- 기술 면접관: MuJoCo/Gymnasium-Robotics 로봇팔 렌더 확인과 Franka/Panda 통합을 별도 기술 단계로 분리했다.
- 개발자/학습자: 먼저 Fetch 예제로 시뮬레이터와 로봇팔 렌더를 확인하고, 이후 Franka asset 통합으로 확장하는 순서를 제시했다.

### 검증 상태
- 검증 완료: FetchPickAndPlace-v4 스냅샷 생성, 로봇팔 렌더 테스트, 전체 pytest 통과
- 검증 불가: Franka/Panda는 asset과 환경이 없어 아직 검증 불가
- 가정: 현재 단계에서는 Fetch 예제로 MuJoCo 로봇팔 렌더 가능 여부를 확인한다.
---
