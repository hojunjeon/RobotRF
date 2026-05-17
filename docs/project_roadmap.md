# Robot Sorting RL 실행 로드맵

현재 프로젝트의 기본 목표는 MuJoCo `FetchSideBinPlace-v0` 환경에서 로봇팔이 정면 테이블 위 물체를 집어 오른쪽 측면의 물리 bin 안에 넣는 것이다. 학습은 Stable-Baselines3 `SAC + HER`와 sparse reward를 기본으로 유지한다.

`FetchPickAndPlace-v4`는 Gymnasium-Robotics baseline으로 남겨 비교 실험에 사용한다.

## 1. 환경 구분

| 용도 | 환경 | Python |
| --- | --- | --- |
| 긴 학습 | WSL Ubuntu | `/home/ubuntu/.venvs/rrf/bin/python` |
| 영상 생성/지표 검증 | Windows PowerShell | `.\.venv-win\Scripts\python.exe` |

Repository-root `.venv`와 `.venv-wsl`은 사용하지 않는다.

## 2. 학습 전 확인

Windows PowerShell:

```powershell
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/check_runtime.py"
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python -m pytest tests/test_side_bin_place_env.py tests/test_robotics_training_path.py tests/test_check_runtime_script.py -q"
```

정상 기준:

- MuJoCo import 성공
- `FetchSideBinPlace-v0` reset/render 성공
- observation keys: `observation`, `achieved_goal`, `desired_goal`
- render shape `(480, 480, 3)`
- 관련 pytest 통과

## 3. 학습 시작

```powershell
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/train.py --env-id FetchSideBinPlace-v0 --algo sac --total-timesteps 2000000 --seed 42 --output-dir checkpoints/side_bin_wsl_2m --tensorboard-log runs/side_bin_wsl_2m --checkpoint-interval 250000 --log-interval-steps 10000"
```

기록할 값:

- env id: `FetchSideBinPlace-v0`
- algorithm: `SAC + HER`
- seed: `42`
- total timesteps: `2000000`
- checkpoint path: `checkpoints/side_bin_wsl_2m/FetchSideBinPlace_v0_sac.zip`
- TensorBoard path: `runs/side_bin_wsl_2m`

초기 성공률이 오래 `0.0`이어도 sparse reward 환경에서는 이상 현상으로 단정하지 않는다. 계획한 timestep까지 학습한 뒤 평가와 영상으로 확인한다.

## 4. 평가

```powershell
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/evaluate.py --env-id FetchSideBinPlace-v0 --checkpoint checkpoints/side_bin_wsl_2m/FetchSideBinPlace_v0_sac.zip --episodes 100 --output evals/side_bin_results.json"
```

성능 지표:

- `episodes`
- `success_rate`
- `mean_reward`
- `mean_episode_length`

성공 판정은 물체 중심이 오른쪽 bin 내부에 있고, 그 상태를 짧게 유지했을 때 `info["is_success"] == 1.0`이 되는 기준이다.

## 5. 영상 생성

```powershell
.\.venv-win\Scripts\python.exe scripts\record_video.py --env-id FetchSideBinPlace-v0 --checkpoint checkpoints\side_bin_wsl_2m\FetchSideBinPlace_v0_sac.zip --output videos\side_bin_wsl_2m_rollout.mp4 --max-steps 50 --start-delay-seconds 1 --end-delay-seconds 1 --fps 25
```

영상에서 확인할 것:

- 물체가 정면 테이블 위에서 시작하는지
- 오른쪽 측면에 물리 bin이 보이는지
- 물체가 bin 벽을 통과하지 않고 내부에 들어가는지
- 최종 성공률과 영상 동작이 서로 모순되지 않는지

## 6. TensorBoard

```powershell
.\.venv-win\Scripts\tensorboard.exe --logdir runs\side_bin_wsl_2m
```

브라우저:

```text
http://localhost:6006
```

## 7. 추후 개선 방안

- Shaped reward 실험: gripper-object 거리, 들어올림, bin 접근, bin 내부 유지 보상을 단계적으로 추가한다.
- 시작 위치 고도화: 정면 고정+작은 랜덤에서 더 넓은 정면 영역 랜덤으로 확장한다.
- Bin 위치 랜덤화: 오른쪽 측면 고정에서 작은 위치 노이즈를 추가해 일반화를 확인한다.
- 성공 유지 step 튜닝: 기본 5 step 유지 기준을 3/5/10 step으로 비교한다.
- 장기 학습 비교: 500K, 1M, 2M, 3M checkpoint별 `success_rate`, `mean_reward`, 영상을 비교한다.
- 영상 기반 검증: 성공률 숫자와 실제 pick-and-place 행동이 일치하는지 rollout 영상으로 확인한다.

## 8. 주의

- Smoke 학습은 실행 경로 증거일 뿐 모델 성능 증거가 아니다.
- Shaped reward는 이번 1차 구현 범위가 아니며, 실제 sparse+HER 결과를 본 뒤 별도 실험으로 추가한다.
- `FetchPickAndPlace-v4` 결과와 `FetchSideBinPlace-v0` 결과를 직접 비교할 때는 환경 목표가 다르다는 점을 명시한다.
