# 새 PC 환경 구성 가이드

이 문서는 다른 PC에서 MuJoCo `FetchPickAndPlace-v4` 기반 학습/평가/영상 생성 경로를 재현하기 위한 절차다. 현재 프로젝트의 기준 경로는 다음과 같다.

- 학습: WSL Ubuntu, `/home/ubuntu/.venvs/rrf`
- 평가: WSL 또는 Windows
- 영상 생성: Windows PowerShell, `.venv-win`
- 기본 환경: `FetchPickAndPlace-v4`
- 알고리즘: Stable-Baselines3 `SAC` + `HerReplayBuffer`

Docker 이미지는 이 문서의 기본 경로가 아니다. NVIDIA 드라이버, WSL2 GPU, Windows 영상 생성은 host PC 설정에 의존하므로 먼저 이 가이드로 native 환경을 검증한다.

## 1. 준비물

Windows PC:

- Windows 11 권장
- NVIDIA GPU와 최신 NVIDIA 드라이버
- WSL2
- Ubuntu 22.04 WSL 배포판
- Git
- Python 3.10 이상

검증된 현재 기준:

- WSL 배포판: `Ubuntu-22.04`
- WSL Python: `3.10.12`
- WSL 학습 venv: `/home/ubuntu/.venvs/rrf`
- MuJoCo: `3.8.1`
- 기본 env id: `FetchPickAndPlace-v4`

## 2. 저장소 준비

Windows PowerShell에서 저장소를 받을 위치로 이동한 뒤 clone한다.

```powershell
git clone <REPOSITORY_URL> RRF
cd RRF
```

이미 저장소를 받은 상태라면 해당 경로로 이동한다.

```powershell
cd C:\Users\<USER>\Desktop\RRF
```

이후 명령의 `C:\Users\<USER>\Desktop\RRF`와 `/mnt/c/Users/<USER>/Desktop/RRF`는 실제 저장소 경로에 맞게 바꾼다.

## 3. Windows 환경 구성

Windows 환경은 짧은 검증, 평가, TensorBoard, MP4 영상 생성에 사용한다.

PowerShell:

```powershell
python -m venv .venv-win
.\.venv-win\Scripts\python.exe -m pip install --upgrade pip
.\.venv-win\Scripts\python.exe -m pip install -e .[dev]
```

Windows runtime을 확인한다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_windows_bootstrap.ps1
.\.venv-win\Scripts\python.exe scripts\check_runtime.py
.\.venv-win\Scripts\python.exe -m pytest
.\.venv-win\Scripts\python.exe -m ruff check .
.\.venv-win\Scripts\python.exe -m pip check
```

기대 기준:

- `FetchPickAndPlace-v4` 생성 성공
- MuJoCo import 성공
- render shape 출력
- pytest 통과
- ruff 통과
- pip dependency conflict 없음

## 4. WSL GPU 확인

PowerShell에서 WSL 배포판을 확인한다.

```powershell
wsl --list --all --verbose
```

Ubuntu 22.04가 없다면 설치한다.

```powershell
wsl --install -d Ubuntu-22.04
```

WSL 내부에서 GPU가 보이는지 확인한다.

```powershell
wsl -- bash -lc "nvidia-smi"
```

`nvidia-smi`가 실패하면 프로젝트 의존성을 설치하기 전에 Windows NVIDIA 드라이버, WSL2, GPU passthrough 상태를 먼저 고친다.

## 5. WSL 학습 환경 구성

WSL에서 저장소 경로와 Python을 확인한다.

```powershell
wsl -- bash -lc "cd /mnt/c/Users/<USER>/Desktop/RRF && pwd && python3 --version && which python3"
```

WSL-native venv를 만든다. 저장소 루트 아래 `.venv-wsl`은 사용하지 않는다.

```powershell
wsl -- bash -lc "mkdir -p ~/.venvs && python3 -m venv ~/.venvs/rrf"
wsl -- bash -lc "~/.venvs/rrf/bin/python -m pip install --upgrade pip"
wsl -- bash -lc "~/.venvs/rrf/bin/python -m pip install -e '/mnt/c/Users/<USER>/Desktop/RRF[dev]'"
```

WSL runtime을 검증한다.

```powershell
wsl -- bash -lc "cd /mnt/c/Users/<USER>/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/check_runtime.py"
wsl -- bash -lc "cd /mnt/c/Users/<USER>/Desktop/RRF && ~/.venvs/rrf/bin/python -m pytest tests/test_robotics_training_path.py tests/test_check_runtime_script.py -q"
wsl -- bash -lc "cd /mnt/c/Users/<USER>/Desktop/RRF && ~/.venvs/rrf/bin/python -m pip check"
```

기대 기준:

- `cuda_available: True`
- MuJoCo import 성공
- `FetchPickAndPlace-v4` reset/render 성공
- render shape `(480, 480, 3)`
- 관련 pytest 통과
- pip dependency conflict 없음

`cuda_available: False`이면 학습은 CPU로 매우 느려진다. 이 경우 PyTorch가 CPU build로 설치됐거나 WSL GPU 연결이 깨진 상태일 수 있으므로, PyTorch CUDA wheel과 NVIDIA/WSL 설정을 다시 확인한다.

## 6. Smoke 학습

긴 학습 전에 10 timestep으로 실행 경로만 확인한다. 이 결과는 모델 성능 증거가 아니다.

```powershell
wsl -- bash -lc "cd /mnt/c/Users/<USER>/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/train.py --env-id FetchPickAndPlace-v4 --algo sac --total-timesteps 10 --seed 42 --output-dir checkpoints/fetch_smoke --tensorboard-log runs/fetch_smoke"
```

checkpoint가 생성되는지 확인한다.

```powershell
dir checkpoints\fetch_smoke
```

예상 checkpoint:

```text
checkpoints\fetch_smoke\FetchPickAndPlace_v4_sac.zip
```

## 7. 긴 학습 시작

Smoke 경로가 통과한 뒤 WSL에서 긴 학습을 시작한다.

```powershell
wsl -- bash -lc "cd /mnt/c/Users/<USER>/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/train.py --env-id FetchPickAndPlace-v4 --algo sac --total-timesteps 2000000 --seed 42 --output-dir checkpoints/fetch_wsl_2m --tensorboard-log runs/fetch_wsl_2m --checkpoint-interval 500000 --log-interval-steps 10000"
```

위 명령은 단일 환경 baseline이다. PC 자원을 더 적극적으로 쓰는 병렬 환경 학습은 별도 output/log 경로로 실행한다.

```powershell
wsl -- bash -lc "cd /mnt/c/Users/<USER>/Desktop/RRF && OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 ~/.venvs/rrf/bin/python scripts/train.py --env-id FetchPickAndPlace-v4 --algo sac --total-timesteps 2000000 --seed 42 --output-dir checkpoints/fetch_wsl_vec6_2m --tensorboard-log runs/fetch_wsl_vec6_2m --n-envs 6 --batch-size 512 --buffer-size 1000000 --gradient-steps -1 --learning-starts 10000 --n-sampled-goal 4 --log-interval-steps 10000 --checkpoint-interval 500000"
```

기록할 값:

- env id: `FetchPickAndPlace-v4`
- algorithm: `SAC + HER`
- seed: `42`
- total timesteps: `2000000`
- checkpoint path: `checkpoints/fetch_wsl_2m/FetchPickAndPlace_v4_sac.zip`
- interval checkpoints: `checkpoints/fetch_wsl_2m/FetchPickAndPlace_v4_sac_500000_steps.zip`, `..._1000000_steps.zip`, `..._1500000_steps.zip`, `..._2000000_steps.zip`
- TensorBoard path: `runs/fetch_wsl_2m`
- parallel checkpoint path: `checkpoints/fetch_wsl_vec6_2m/FetchPickAndPlace_v4_sac.zip`
- parallel TensorBoard path: `runs/fetch_wsl_vec6_2m`
- resume command option: `--resume-from checkpoints/fetch_wsl_vec6_2m/FetchPickAndPlace_v4_sac.zip`

주의:

- `500000` timestep은 로봇 sparse reward 환경에서 충분하지 않을 수 있으므로, 기본 장기 학습은 `2000000` timestep으로 잡고 `500000`마다 checkpoint를 저장한다.
- 초기 성공률은 오래 `0.0`일 수 있다.
- smoke 학습 성공은 실행 경로 증거이지 정책 성능 증거가 아니다.
- 병렬 학습은 한 policy가 여러 환경에서 샘플을 모으는 방식이며, timestep 진행 로그를 `timesteps: 10000/500000` 형식으로 출력한다.

## 8. 평가

학습 후 WSL에서 평가한다.

```powershell
wsl -- bash -lc "cd /mnt/c/Users/<USER>/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/evaluate.py --env-id FetchPickAndPlace-v4 --checkpoint checkpoints/fetch_wsl_2m/FetchPickAndPlace_v4_sac.zip --episodes 100 --output evals/fetch_results.json"
```

평가 결과에서 기록할 값:

- `episodes`
- `success_rate`
- `mean_reward`
- `mean_episode_length`

평가 결과는 `evals/fetch_results.json` 파일에 누적 저장된다.

## 9. 영상 생성

MP4 rollout은 Windows에서 생성한다.

```powershell
.\.venv-win\Scripts\python.exe scripts\record_video.py --env-id FetchPickAndPlace-v4 --checkpoint checkpoints\fetch_wsl_2m\FetchPickAndPlace_v4_sac.zip --output videos\fetch_wsl_2m_rollout.mp4 --max-steps 50
```

출력 파일:

```text
videos\fetch_wsl_500k_rollout.mp4
```

## 10. TensorBoard

Windows PowerShell:

```powershell
.\.venv-win\Scripts\tensorboard.exe --logdir runs\fetch_wsl_2m
```

브라우저:

```text
http://localhost:6006
```

## 11. 문제 해결 체크리스트

`ModuleNotFoundError`:

- 올바른 venv의 Python을 쓰는지 확인한다.
- Windows: `.\.venv-win\Scripts\python.exe`
- WSL: `~/.venvs/rrf/bin/python`
- `pip install -e .[dev]`를 다시 실행한다.

`FetchPickAndPlace-v4` 생성 실패:

- `gymnasium-robotics`가 설치됐는지 확인한다.
- `scripts/check_runtime.py`를 먼저 실행한다.

`cuda_available: False`:

- Windows에서 NVIDIA 드라이버를 확인한다.
- WSL에서 `nvidia-smi`를 확인한다.
- PyTorch CUDA build가 설치됐는지 확인한다.

MuJoCo render 실패:

- WSL 학습 검증과 Windows 영상 생성을 분리해서 확인한다.
- 먼저 `scripts/check_runtime.py`가 render shape를 출력하는지 본다.

학습 성공률이 계속 `0.0`:

- 환경 구성 실패로 단정하지 않는다.
- Fetch pick-and-place는 sparse reward라 초반 성공률이 오래 0일 수 있다.
- checkpoint, TensorBoard log, seed, timesteps, 평가 episodes를 함께 기록한다.

## 12. Docker를 나중에 추가할 때의 기준

Docker는 다음 조건이 생겼을 때 추가한다.

- 여러 Linux 학습 PC에서 같은 의존성 설치를 반복해야 한다.
- WSL-native venv 설치 시간이 실제 병목이다.
- Windows 영상 생성은 native로 유지해도 된다.

Docker를 추가하더라도 범위는 `Dockerfile.train` 같은 Linux 학습 전용 이미지로 제한한다. NVIDIA 드라이버, NVIDIA Container Toolkit, host GPU 확인은 별도 host 설정으로 남는다.
