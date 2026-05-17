# FetchSideBinPlace-v0 학습/평가/영상 생성 명령어

이 문서는 오른쪽 물리 bin 환경인 `FetchSideBinPlace-v0`를 기준으로 한다. 학습은 WSL Ubuntu에서 실행하고, 영상 생성은 Windows PowerShell에서 실행한다.

Smoke 성공은 실행 경로 증거일 뿐 모델 성능 증거가 아니다. 최종 성능은 평가 JSON과 rollout 영상으로 확인한다.

## 1. 학습 전 확인

Windows PowerShell:

```powershell
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/check_runtime.py"
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python -m pytest tests/test_side_bin_place_env.py tests/test_robotics_training_path.py tests/test_check_runtime_script.py tests/test_training_defaults.py -q"
```

## 2. 학습 시작

단일 환경 장기 학습:

```powershell
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/train.py --env-id FetchSideBinPlace-v0 --algo sac --total-timesteps 2000000 --seed 42 --output-dir checkpoints/side_bin_wsl_2m --tensorboard-log runs/side_bin_wsl_2m --checkpoint-interval 250000 --log-interval-steps 10000"
```

병렬 환경 장기 학습:

```powershell
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 ~/.venvs/rrf/bin/python scripts/train.py --env-id FetchSideBinPlace-v0 --algo sac --total-timesteps 2000000 --seed 42 --output-dir checkpoints/side_bin_wsl_vec6_2m --tensorboard-log runs/side_bin_wsl_vec6_2m --n-envs 6 --batch-size 512 --buffer-size 1000000 --gradient-steps -1 --learning-starts 10000 --n-sampled-goal 4 --log-interval-steps 10000 --checkpoint-interval 250000"
```

기록할 값:

- env id: `FetchSideBinPlace-v0`
- algorithm: `SAC + HER`
- seed: `42`
- total timesteps: `2000000`
- checkpoint interval: `250000`
- 단일 학습 checkpoint: `checkpoints/side_bin_wsl_2m/FetchSideBinPlace_v0_sac.zip`
- 병렬 학습 checkpoint: `checkpoints/side_bin_wsl_vec6_2m/FetchSideBinPlace_v0_sac.zip`
- TensorBoard log: `runs/side_bin_wsl_2m` 또는 `runs/side_bin_wsl_vec6_2m`

## 3. TensorBoard 확인

Windows PowerShell:

```powershell
.\.venv-win\Scripts\tensorboard.exe --logdir runs\side_bin_wsl_2m
```

병렬 학습 로그를 볼 때:

```powershell
.\.venv-win\Scripts\tensorboard.exe --logdir runs\side_bin_wsl_vec6_2m
```

브라우저:

```text
http://localhost:6006
```

## 4. 학습 종료 후 평가

단일 환경 최종 checkpoint 평가:

```powershell
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/evaluate.py --env-id FetchSideBinPlace-v0 --checkpoint checkpoints/side_bin_wsl_2m/FetchSideBinPlace_v0_sac.zip --episodes 100 --output evals/side_bin_results.json"
```

병렬 환경 최종 checkpoint 평가:

```powershell
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/evaluate.py --env-id FetchSideBinPlace-v0 --checkpoint checkpoints/side_bin_wsl_vec6_2m/FetchSideBinPlace_v0_sac.zip --episodes 100 --output evals/side_bin_results.json"
```

평가 JSON에서 확인할 값:

- `episodes`
- `success_rate`
- `mean_reward`
- `mean_episode_length`

## 5. 최종 checkpoint 영상 생성

단일 환경 최종 checkpoint:

```powershell
.\.venv-win\Scripts\python.exe scripts\record_video.py --env-id FetchSideBinPlace-v0 --checkpoint checkpoints\side_bin_wsl_2m\FetchSideBinPlace_v0_sac.zip --output videos\side_bin_wsl_2m_rollout.mp4 --max-steps 50 --start-delay-seconds 1 --end-delay-seconds 1 --fps 25
```

병렬 환경 최종 checkpoint:

```powershell
.\.venv-win\Scripts\python.exe scripts\record_video.py --env-id FetchSideBinPlace-v0 --checkpoint checkpoints\side_bin_wsl_vec6_2m\FetchSideBinPlace_v0_sac.zip --output videos\side_bin_wsl_vec6_2m_rollout.mp4 --max-steps 50 --start-delay-seconds 1 --end-delay-seconds 1 --fps 25
```

## 6. 250K 단위 checkpoint 영상 생성

아래 명령은 병렬 환경 장기 학습 산출물인 `checkpoints\side_bin_wsl_vec6_2m` 기준이다. 단일 환경 산출물을 영상화하려면 경로의 `side_bin_wsl_vec6_2m`를 `side_bin_wsl_2m`로 바꾼다.

```powershell
.\.venv-win\Scripts\python.exe scripts\record_video.py --env-id FetchSideBinPlace-v0 --checkpoint checkpoints\side_bin_wsl_vec6_2m\FetchSideBinPlace_v0_sac_250000_steps.zip --output videos\side_bin_wsl_vec6_2m_250000_steps.mp4 --max-steps 50 --start-delay-seconds 1 --end-delay-seconds 1 --fps 25
.\.venv-win\Scripts\python.exe scripts\record_video.py --env-id FetchSideBinPlace-v0 --checkpoint checkpoints\side_bin_wsl_vec6_2m\FetchSideBinPlace_v0_sac_500000_steps.zip --output videos\side_bin_wsl_vec6_2m_500000_steps.mp4 --max-steps 50 --start-delay-seconds 1 --end-delay-seconds 1 --fps 25
.\.venv-win\Scripts\python.exe scripts\record_video.py --env-id FetchSideBinPlace-v0 --checkpoint checkpoints\side_bin_wsl_vec6_2m\FetchSideBinPlace_v0_sac_750000_steps.zip --output videos\side_bin_wsl_vec6_2m_750000_steps.mp4 --max-steps 50 --start-delay-seconds 1 --end-delay-seconds 1 --fps 25
.\.venv-win\Scripts\python.exe scripts\record_video.py --env-id FetchSideBinPlace-v0 --checkpoint checkpoints\side_bin_wsl_vec6_2m\FetchSideBinPlace_v0_sac_1000000_steps.zip --output videos\side_bin_wsl_vec6_2m_1000000_steps.mp4 --max-steps 50 --start-delay-seconds 1 --end-delay-seconds 1 --fps 25
.\.venv-win\Scripts\python.exe scripts\record_video.py --env-id FetchSideBinPlace-v0 --checkpoint checkpoints\side_bin_wsl_vec6_2m\FetchSideBinPlace_v0_sac_1250000_steps.zip --output videos\side_bin_wsl_vec6_2m_1250000_steps.mp4 --max-steps 50 --start-delay-seconds 1 --end-delay-seconds 1 --fps 25
.\.venv-win\Scripts\python.exe scripts\record_video.py --env-id FetchSideBinPlace-v0 --checkpoint checkpoints\side_bin_wsl_vec6_2m\FetchSideBinPlace_v0_sac_1500000_steps.zip --output videos\side_bin_wsl_vec6_2m_1500000_steps.mp4 --max-steps 50 --start-delay-seconds 1 --end-delay-seconds 1 --fps 25
.\.venv-win\Scripts\python.exe scripts\record_video.py --env-id FetchSideBinPlace-v0 --checkpoint checkpoints\side_bin_wsl_vec6_2m\FetchSideBinPlace_v0_sac_1750000_steps.zip --output videos\side_bin_wsl_vec6_2m_1750000_steps.mp4 --max-steps 50 --start-delay-seconds 1 --end-delay-seconds 1 --fps 25
.\.venv-win\Scripts\python.exe scripts\record_video.py --env-id FetchSideBinPlace-v0 --checkpoint checkpoints\side_bin_wsl_vec6_2m\FetchSideBinPlace_v0_sac_2000000_steps.zip --output videos\side_bin_wsl_vec6_2m_2000000_steps.mp4 --max-steps 50 --start-delay-seconds 1 --end-delay-seconds 1 --fps 25
```

## 7. 250K 단위 checkpoint 평가

필요할 때만 실행한다. 결과는 같은 `evals/side_bin_results.json`에 누적 저장된다.

```powershell
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/evaluate.py --env-id FetchSideBinPlace-v0 --checkpoint checkpoints/side_bin_wsl_vec6_2m/FetchSideBinPlace_v0_sac_250000_steps.zip --episodes 100 --output evals/side_bin_results.json"
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/evaluate.py --env-id FetchSideBinPlace-v0 --checkpoint checkpoints/side_bin_wsl_vec6_2m/FetchSideBinPlace_v0_sac_500000_steps.zip --episodes 100 --output evals/side_bin_results.json"
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/evaluate.py --env-id FetchSideBinPlace-v0 --checkpoint checkpoints/side_bin_wsl_vec6_2m/FetchSideBinPlace_v0_sac_750000_steps.zip --episodes 100 --output evals/side_bin_results.json"
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/evaluate.py --env-id FetchSideBinPlace-v0 --checkpoint checkpoints/side_bin_wsl_vec6_2m/FetchSideBinPlace_v0_sac_1000000_steps.zip --episodes 100 --output evals/side_bin_results.json"
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/evaluate.py --env-id FetchSideBinPlace-v0 --checkpoint checkpoints/side_bin_wsl_vec6_2m/FetchSideBinPlace_v0_sac_1250000_steps.zip --episodes 100 --output evals/side_bin_results.json"
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/evaluate.py --env-id FetchSideBinPlace-v0 --checkpoint checkpoints/side_bin_wsl_vec6_2m/FetchSideBinPlace_v0_sac_1500000_steps.zip --episodes 100 --output evals/side_bin_results.json"
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/evaluate.py --env-id FetchSideBinPlace-v0 --checkpoint checkpoints/side_bin_wsl_vec6_2m/FetchSideBinPlace_v0_sac_1750000_steps.zip --episodes 100 --output evals/side_bin_results.json"
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/evaluate.py --env-id FetchSideBinPlace-v0 --checkpoint checkpoints/side_bin_wsl_vec6_2m/FetchSideBinPlace_v0_sac_2000000_steps.zip --episodes 100 --output evals/side_bin_results.json"
```

## 8. 영상에서 확인할 것

- 물체가 로봇 정면 테이블 위에서 시작하는지
- 오른쪽 측면에 파란 물리 bin이 보이는지
- 물체가 bin 벽을 통과하지 않고 내부에 들어가는지
- 평가 `success_rate`와 rollout 영상의 실제 행동이 서로 모순되지 않는지
