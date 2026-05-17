# 병렬 학습 준비사항

이 문서는 기존 단일 환경 학습을 baseline으로 보존한 뒤, `FetchPickAndPlace-v4` 병렬 환경 학습을 시작하기 전에 확인할 항목을 정리한다.

## 1. 시작 전 원칙

- 현재 진행 중인 단일 학습은 끝까지 완료한다.
- 단일 baseline의 checkpoint, TensorBoard log, 평가 JSON, rollout 영상을 먼저 확보한다.
- 병렬 학습은 baseline과 다른 output/log 경로를 사용한다.
- 단일 학습과 병렬 학습을 동시에 돌리지 않는다. CPU/GPU/RAM/I/O 자원 경쟁 때문에 비교 조건이 흐려진다.

## 2. 단일 baseline 완료 후 저장할 증거

평가 결과는 하나의 JSON 파일에 누적 저장한다.

```powershell
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/evaluate.py --env-id FetchPickAndPlace-v4 --checkpoint checkpoints/fetch_wsl_2m/FetchPickAndPlace_v4_sac.zip --episodes 100 --output evals/fetch_results.json"
```

영상 생성:

```powershell
.\.venv-win\Scripts\python.exe scripts\record_video.py --env-id FetchPickAndPlace-v4 --checkpoint checkpoints\fetch_wsl_2m\FetchPickAndPlace_v4_sac.zip --output videos\fetch_wsl_2m_rollout.mp4 --max-steps 50 --start-delay-seconds 1 --end-delay-seconds 1 --fps 25
```

기록할 값:

- env id: `FetchPickAndPlace-v4`
- algorithm: `SAC + HER`
- seed: `42`
- timesteps: `2000000`
- checkpoint: `checkpoints/fetch_wsl_2m/FetchPickAndPlace_v4_sac.zip`
- interval checkpoints: `checkpoints/fetch_wsl_2m/FetchPickAndPlace_v4_sac_250000_steps.zip`, `..._500000_steps.zip`, `..._750000_steps.zip`, `..._1000000_steps.zip`
- TensorBoard log: `runs/fetch_wsl_2m`
- evaluation output: `evals/fetch_results.json`
- video: `videos/fetch_wsl_2m_rollout.mp4`

## 3. 병렬 학습 실행 전 확인

WSL runtime:

```powershell
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/check_runtime.py"
```

기대 기준:

- `cuda_available: True`
- `FetchPickAndPlace-v4` reset/render 성공
- render shape `(480, 480, 3)`

병렬 smoke:

```powershell
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/train.py --env-id FetchPickAndPlace-v4 --algo sac --total-timesteps 20 --seed 42 --output-dir checkpoints/parallel_autostart_smoke_wsl --tensorboard-log runs/parallel_autostart_smoke_wsl --n-envs 2 --batch-size 256 --gradient-steps 1 --log-interval-steps 10"
```

기대 로그:

```text
Using cuda device
timesteps: 10/20
timesteps: 20/20
saved checkpoint: checkpoints/parallel_autostart_smoke_wsl/FetchPickAndPlace_v4_sac.zip
```

## 4. 병렬 학습 명령

```powershell
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 ~/.venvs/rrf/bin/python scripts/train.py --env-id FetchPickAndPlace-v4 --algo sac --total-timesteps 2000000 --seed 42 --output-dir checkpoints/fetch_wsl_vec6_2m --tensorboard-log runs/fetch_wsl_vec6_2m --n-envs 6 --batch-size 512 --buffer-size 1000000 --gradient-steps -1 --learning-starts 10000 --n-sampled-goal 4 --log-interval-steps 10000 --checkpoint-interval 250000"
```

이 명령은 하나의 SAC policy가 6개 MuJoCo 환경에서 샘플을 모으는 방식이다. Isaac Lab처럼 한 화면에 여러 로봇이 동시에 렌더링되는 방식은 아니다.
`--checkpoint-interval 250000`은 병렬 환경 수와 무관하게 실제 누적 timestep 기준으로 동작하므로, `250000`, `500000`, `750000`, `1000000` step처럼 250K 단위 checkpoint가 저장된다.

## 5. 병렬 checkpoint에서 이어학습

주말 학습 결과가 부족하면 최종 checkpoint에서 이어서 추가 학습한다. 아래 명령은 기존 `fetch_wsl_vec6_2m` checkpoint를 불러와 1M timestep을 더 학습하고, 새 checkpoint는 `fetch_wsl_vec6_3m`에 저장한다.

```powershell
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 ~/.venvs/rrf/bin/python scripts/train.py --env-id FetchPickAndPlace-v4 --algo sac --total-timesteps 1000000 --seed 42 --output-dir checkpoints/fetch_wsl_vec6_3m --tensorboard-log runs/fetch_wsl_vec6_2m --n-envs 6 --batch-size 512 --buffer-size 1000000 --gradient-steps -1 --learning-starts 10000 --n-sampled-goal 4 --log-interval-steps 10000 --checkpoint-interval 250000 --resume-from checkpoints/fetch_wsl_vec6_2m/FetchPickAndPlace_v4_sac.zip"
```

## 6. 병렬 학습 후 평가

같은 JSON 파일에 평가 결과를 이어서 저장한다.

```powershell
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/evaluate.py --env-id FetchPickAndPlace-v4 --checkpoint checkpoints/fetch_wsl_vec6_2m/FetchPickAndPlace_v4_sac.zip --episodes 100 --output evals/fetch_results.json"
```

영상 생성:

```powershell
.\.venv-win\Scripts\python.exe scripts\record_video.py --env-id FetchPickAndPlace-v4 --checkpoint checkpoints\fetch_wsl_vec6_2m\FetchPickAndPlace_v4_sac.zip --output videos\fetch_wsl_vec6_2m_rollout.mp4 --max-steps 50 --start-delay-seconds 1 --end-delay-seconds 1 --fps 25
```

## 7. 비교 기준

최소 비교 항목:

- `success_rate`
- `mean_reward`
- `mean_episode_length`
- 학습 `total_timesteps`
- 학습 wall-clock time
- TensorBoard `fps`
- 영상에서 실제 pick-and-place 동작이 보이는지

동일하게 맞출 조건:

- env id: `FetchPickAndPlace-v4`
- seed: `42`
- train timesteps: `2000000`
- evaluation episodes: `100`

## 8. 주의사항

- 병렬 학습은 GPU 사용률을 올릴 수 있지만, 성능 향상을 보장하지 않는다.
- `--resume-from`은 저장된 policy checkpoint에서 가중치를 이어받는다. replay buffer 전체를 복원하는 완전 재개 기능은 아니다.
- `learning_starts`가 너무 작으면 HER가 첫 episode 종료 전 sampling을 시도해 실패할 수 있다. 병렬 학습 추천 명령은 `--learning-starts 10000`을 사용한다.
- smoke checkpoint는 실행 경로 증거이지 성능 증거가 아니다.
- 최종 주장은 평가 JSON과 rollout 영상이 나온 뒤에만 한다.
