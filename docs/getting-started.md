# 시작하기

## 설치

Moru Marketplace를 등록하고 플러그인을 설치합니다.

```powershell
codex plugin marketplace add IncleRepo/moru --ref main
codex plugin add moru@moru
```

설치 후에는 새 대화를 시작해야 합니다. 다음 명령에서 `moru@moru`가 `installed, enabled`로 표시되면 사용할 준비가 된 상태입니다.

```powershell
codex plugin list
```

## 사용

처리할 요청 앞에 `$moru`를 붙입니다.

```text
$moru 로그인 실패 원인을 찾고 수정한 뒤 관련 테스트까지 실행해줘.
```

작업 범위와 제한도 같은 요청에 적습니다.

```text
$moru 이 변경사항을 리뷰만 해줘. 파일은 수정하지 마.
```

Moru는 요청한 결과를 기준으로 필요한 조사, 구현, 검증을 이어서 수행합니다. 프로젝트에 `MORU.md`가 있으면 등록된 규칙과 자료도 함께 확인합니다.

## 결과 상태

- `COMPLETE`: 요청한 결과와 필요한 검증이 끝남
- `PARTIAL`: 일부 결과는 끝났지만 독립된 나머지 작업을 완료하지 못함
- `BLOCKED`: 필수 정보, 접근 권한 또는 기능이 없어 결과를 만들 수 없음

상태와 함께 변경 내용, 확인한 결과, 남은 일이 보고됩니다.

## 업데이트

Marketplace를 갱신하고 Moru를 다시 설치합니다.

```powershell
codex plugin marketplace upgrade moru
codex plugin add moru@moru
```

업데이트한 버전은 새 대화부터 적용됩니다.

다음 단계로 [프로젝트와 스킬 설정](./project-setup.md)을 참고하세요.
