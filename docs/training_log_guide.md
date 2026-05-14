# 학습 로그 해석 가이드

이 문서는 Stable-Baselines3가 출력하는 MuJoCo `FetchPickAndPlace-v4` 학습 로그를 비전공자도 읽을 수 있게 정리한 설명이다. 숫자는 모델의 "중간 건강검진"에 가깝다. 한 줄만 보고 성공/실패를 판단하지 말고, 같은 항목의 추세와 최종 평가 결과를 함께 봐야 한다.

예시 로그:

```text
---------------------------------
| rollout/           |          |
|    ep_len_mean     | 50       |
|    ep_rew_mean     | -48      |
|    success_rate    | 0.04     |
| time/              |          |
|    episodes        | 3108     |
|    fps             | 33       |
|    time_elapsed    | 4600     |
|    total_timesteps | 155400   |
| train/             |          |
|    actor_loss      | 3.96     |
|    critic_loss     | 0.214    |
|    ent_coef        | 0.00176  |
|    ent_coef_loss   | 3.48     |
|    learning_rate   | 0.0003   |
|    n_updates       | 155299   |
---------------------------------
```

## 먼저 봐야 할 항목

### `success_rate`

최근 episode에서 목표를 성공한 비율이다.

- `0.00`: 최근 구간에서 성공 없음
- `0.04`: 최근 구간 성공률 4%
- `1.00`: 최근 구간 성공률 100%

`FetchPickAndPlace-v4`는 sparse reward 환경이라 초반에는 `0.00`이 오래 나올 수 있다. `155400` timestep에서 `0.04`가 나왔다는 것은 아직 좋은 정책은 아니지만, 성공 샘플이 조금씩 생기기 시작했다는 뜻으로 볼 수 있다.

### `ep_rew_mean`

최근 episode 평균 reward다.

Fetch 계열 sparse reward에서는 보통 실패 step마다 `-1`, 성공 상태에서는 `0`에 가까운 보상을 받는다. episode 최대 길이가 50이고 `ep_rew_mean=-48`이면, 대부분 step은 아직 실패지만 일부 성공 구간이 섞였다는 뜻이다.

### `total_timesteps`

지금까지 환경과 상호작용한 총 step 수다.

예를 들어 목표가 `500000` timestep이면:

```text
155400 / 500000 = 약 31%
```

아직 학습 중간 상태이므로 최종 성능은 학습 완료 후 평가해야 한다.

### `fps`

초당 처리한 environment step 수다. 학습 속도를 보는 지표다.

- `fps=33`: 초당 약 33 step 처리
- 값이 높을수록 wall-clock 기준 학습이 빠르게 진행된다.

단일 MuJoCo 환경은 CPU simulation 병목이 있어서 GPU 사용률이 낮아 보여도 `fps`가 크게 오르지 않을 수 있다. 병렬 환경 학습은 여러 environment에서 샘플을 모아 이 병목을 줄이기 위한 실험이다.

## `rollout/` 항목

`rollout/`은 실제 환경에서 policy가 행동하며 수집한 episode 통계다.

| 항목 | 의미 | 읽는 법 |
| --- | --- | --- |
| `ep_len_mean` | 최근 episode 평균 길이 | `50`이면 대부분 episode가 최대 길이까지 진행됨 |
| `ep_rew_mean` | 최근 episode 평균 reward | 0에 가까워질수록 보통 성공 step이 많아진 것 |
| `success_rate` | 최근 episode 성공률 | 가장 직관적인 성능 지표 |

## `time/` 항목

`time/`은 학습 진행량과 속도를 보여준다.

| 항목 | 의미 | 읽는 법 |
| --- | --- | --- |
| `episodes` | 지금까지 끝난 episode 수 | 예시의 `3108`은 3108개 episode 완료 |
| `fps` | 초당 처리 step 수 | 학습 속도 지표 |
| `time_elapsed` | 학습 시작 후 경과 시간, 초 단위 | `4600`초는 약 76분 40초 |
| `total_timesteps` | 누적 environment step | 목표 timestep 대비 진행률 계산에 사용 |

## `train/` 항목

`train/`은 SAC 신경망이 업데이트되는 내부 상태다. 비전공자는 절대값보다 "폭주하는지", "갑자기 이상하게 튀는지" 정도를 보면 된다.

| 항목 | 의미 | 읽는 법 |
| --- | --- | --- |
| `actor_loss` | 행동을 고르는 policy network의 loss | 절대값만으로 좋고 나쁨을 판단하지 않음 |
| `critic_loss` | Q-value를 예측하는 critic network의 loss | 급격한 폭주 여부를 추세로 확인 |
| `ent_coef` | 탐색을 얼마나 장려할지 조절하는 계수 | 낮아질수록 행동이 덜 랜덤해지는 경향 |
| `ent_coef_loss` | entropy coefficient 자동 조정 loss | 직접 성능 지표는 아님 |
| `learning_rate` | 신경망 학습률 | 현재 기본값은 `0.0003` |
| `n_updates` | 신경망 업데이트 횟수 | off-policy SAC에서는 timestep과 비슷하게 증가할 수 있음 |

## 예시 로그 해석

위 예시는 다음처럼 해석한다.

- 진행률: `155400 / 500000`, 약 31%
- 속도: `33 fps`
- 완료 episode: `3108`
- 최근 성공률: `4%`
- 평균 reward: `-48`
- episode 평균 길이: `50`

즉, 이 시점의 모델은 아직 성공률이 낮지만 성공을 전혀 못 하는 상태는 아니다. sparse reward 환경에서는 초반 성공률이 오래 낮을 수 있으므로, 중간 로그만 보고 중단하기보다 계획한 timestep까지 학습한 뒤 평가한다.

## 최종 판단 기준

학습 중 로그는 참고용이고, 최종 판단은 별도 평가 명령으로 한다.

```powershell
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/evaluate.py --env-id FetchPickAndPlace-v4 --checkpoint checkpoints/fetch_wsl_2m/FetchPickAndPlace_v4_sac.zip --episodes 100 --output evals/fetch_results.json"
```

평가 결과에서 우선 볼 항목:

- `success_rate`
- `mean_reward`
- `mean_episode_length`
- 평가 episode 수

기록할 때는 seed, timestep, checkpoint path, TensorBoard path, 평가 episode 수를 함께 남긴다.
