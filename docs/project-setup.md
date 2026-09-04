# 프로젝트와 스킬 설정

## `MORU.md`

프로젝트 루트의 `MORU.md`에는 반복해서 사용할 작업 대상, 요구사항, 규칙, 참고 자료와 전문 스킬을 등록합니다. Moru는 호출될 때 이 파일을 찾아 프로젝트 기본 설정으로 사용합니다.

제목은 정해진 영문 이름을 사용하고 설명은 한국어로 작성해도 됩니다. 필요한 항목만 남기세요.

```markdown
# Moru Project Context

## Targets
- src/
- tests/

## Requirements
- docs/requirements.md — 현재 기준 요구사항

## Policies
- AGENTS.md
- docs/security-policy.md

## Skills
- $backend-conventions — 백엔드 구현과 리뷰에 우선 사용
- $database-safety — 데이터베이스 작업에 우선 사용

## References
- docs/examples/

## Evidence
- https://example.internal/dashboard

## Excluded
- legacy/
```

각 항목의 역할은 다음과 같습니다.

| 항목 | 용도 |
| --- | --- |
| `Targets` | 기본 작업 대상 |
| `Requirements` | 결과가 충족해야 하는 요구사항 |
| `Policies` | 반드시 따라야 하는 프로젝트 규칙 |
| `Skills` | 프로젝트에서 우선 사용할 전문 스킬 |
| `References` | 사례와 배경 자료 |
| `Evidence` | 사실 판단에 사용할 데이터 출처 |
| `Excluded` | 기본 탐색과 변경에서 제외할 영역 |

문서 본문을 복사하지 말고 경로나 링크를 등록하세요. 비밀번호, 토큰, 개인 키는 기록하지 않습니다. 기본 형식은 [MORU.template.md](../plugins/moru/skills/moru/assets/MORU.template.md)에서 복사할 수 있습니다.

## 전문 스킬 준비

프로젝트 전용 절차나 팀 규칙은 Moru 본체가 아니라 독립된 전문 스킬에 둡니다. 이렇게 하면 같은 스킬을 Moru 없이 직접 호출할 수도 있고, 다른 프로젝트에서 재사용하거나 별도로 버전을 관리할 수도 있습니다.

새 스킬이 필요하면 `$skill-creator`로 만들고, GitHub 저장소에 있는 스킬은 `$skill-installer`에 저장소와 경로를 알려 설치할 수 있습니다.

```text
$skill-installer owner/repository의 skills/backend-review 스킬을 설치해줘.
```

플러그인으로 배포되는 스킬은 해당 Marketplace의 설치 방법을 따릅니다. 어떤 방식이든 Codex에 설치한 뒤 새 대화를 시작해야 사용할 수 있습니다.

## 프로젝트 기본 스킬 등록

Codex에 설치된 스킬 중 프로젝트에서 반복해서 사용할 항목만 `Skills`에 적습니다.

```markdown
## Skills
- $backend-conventions — 백엔드 구현과 리뷰에 우선 사용
- $database-safety — 데이터베이스 조회와 변경에 우선 사용
```

Moru의 선택 순서는 다음과 같습니다.

1. 현재 요청에서 사용자가 직접 지정한 적합한 스킬
2. `MORU.md`에 등록된 적합한 프로젝트 기본 스킬
3. 그 밖에 설치된 스킬과 도구 중 작업에 가장 알맞은 것

`Skills`는 허용 목록이 아닙니다. 등록되지 않은 스킬도 작업에 필요하면 선택할 수 있습니다. 반대로 이름을 등록해도 스킬이 자동 설치되거나 데이터 접근과 변경 권한이 생기지는 않습니다. 설치되지 않은 스킬이 꼭 필요하다면 Moru는 그 기능이 없다는 사실과 필요한 조치를 보고합니다.

스킬의 세부 지침을 `MORU.md`에 복사하지 마세요. `MORU.md`에는 이름과 사용 범위만 적고, 실제 절차는 해당 스킬에서 관리합니다.
