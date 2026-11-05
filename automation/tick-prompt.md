이 작업은 jeonck/ai-security-kb 레포의 GitHub Actions를 정시에 깨우는 알람이다. 다른 파일을 읽거나 고치지 않는다.

GitHub MCP 도구 `actions_run_trigger`로 `kb-tick.yml` 워크플로를 `ref: main`에서 `run_workflow` 한다 (inputs 없음). 푸시·강제 푸시는 하지 않는다.
실패하면 한 번만 다시 시도하고, 그래도 실패하면 오류 메시지 첫 줄을 보고한다.

T=$(TZ=America/Chicago date '+%F %H:%M')

보고는 한 줄만 쓴다. 성공하면 "⏰ kb-tick $T CT", 실패하면 "⚠️ kb-tick 실패 $T CT: <이유>".
