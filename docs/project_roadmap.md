# Robot Sorting RL 실행 로드맵

현재 프로젝트는 MuJoCo `FetchPickAndPlace-v4` 로봇팔 환경을 SAC + HER로 학습하고, 저장된 checkpoint를 평가/영상화하는 경로에 집중한다.

## 1. 환경 구분

| 용도 | 환경 | Python |
| --- | --- | --- |
| 긴 학습 | WSL Ubuntu | `/home/ubuntu/.venvs/rrf/bin/python` |
| 영상 생성/짧은 검증 | Windows PowerShell | `.\.venv-win\Scripts\python.exe` |

Repository-root `.venv`와 `.venv-wsl`은 사용하지 않는다.

## 2. 학습 전 확인

Windows PowerShell:

```powershell
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/check_runtime.py"
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python -m pytest tests/test_robotics_training_path.py tests/test_check_runtime_script.py -q"
```

정상 기준:

- MuJoCo import 성공
- `FetchPickAndPlace-v4` reset/render 성공
- render shape `(480, 480, 3)`
- 관련 pytest 통과

## 3. 학습 시작

```powershell
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/train.py --env-id FetchPickAndPlace-v4 --algo sac --total-timesteps 500000 --seed 42 --output-dir checkpoints/fetch_wsl_500k --tensorboard-log runs/fetch_wsl_500k"
```

기록할 값:

- env id: `FetchPickAndPlace-v4`
- algorithm: `SAC + HER`
- seed: `42`
- total timesteps: `500000`
- checkpoint path: `checkpoints/fetch_wsl_500k/FetchPickAndPlace_v4_sac.zip`
- TensorBoard path: `runs/fetch_wsl_500k`

## 4. 평가

```powershell
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/evaluate.py --env-id FetchPickAndPlace-v4 --checkpoint checkpoints/fetch_wsl_500k/FetchPickAndPlace_v4_sac.zip --episodes 100"
```

성능표 지표:

- `episodes`
- `success_rate`
- `mean_reward`
- `mean_episode_length`

## 5. 영상 생성

```powershell
.\.venv-win\Scripts\python.exe scripts\record_video.py --env-id FetchPickAndPlace-v4 --checkpoint checkpoints\fetch_wsl_500k\FetchPickAndPlace_v4_sac.zip --output videos\fetch_wsl_500k_rollout.mp4 --max-steps 50
```

## 6. TensorBoard

```powershell
.\.venv-win\Scripts\tensorboard.exe --logdir runs\fetch_wsl_500k
```

브라우저:

```text
http://localhost:6006
```

## 7. 주의

- 짧은 smoke 학습은 실행 경로 증거일 뿐 성능 증거가 아니다.
- 초기 학습은 sparse reward 때문에 성공률이 오래 `0.0`일 수 있다.
- 현재 프로젝트는 Fetch 예제 환경 중심이다. 분리수거 task나 Franka/Panda custom asset은 별도 통합 작업이다.
