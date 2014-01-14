LR2Server
=========

share your bms file with LR2Server!
LR2Server로 BMS곡을 보다 편하게 공유하세요.


기능
----
* LR2의 db를 읽어서 bms 리스트 표시
* bms 검색 및 필터링 가능
* bms 음원을 자체적으로 인코딩하여 즉시 다운로드 가능
* bms 차분 혹은 bms 음원 전체 archive 다운로드 가능


사용법
------
1. LR2Server을 받아서 LR2body.exe가 있는 폴더에 압축을 풉니다. (LR2Server 디렉토리 안에 파일을 풀 것)
2. start.bat를 실행합니다.
3. 친구들에게 자신의 서버 ip를 알려줍니다.


URL
---
* http://127.0.0.1:8000 -> 모든 BMS을 리스트로 보여줌 (곡이 많을 시 꽤 큰 부담이 될 수 있음)
* http://127.0.0.1:8000/0/ -> BMS를 페이지별로 100곡 씩 나눠서 보여줌 (1페이지)
* http://127.0.0.1:8000/user/kuna/ -> 'kuna'라는 유저의 스코어가 표시된 BMS 리스트를 보여줌.


문제점 및 추가기능구현 예정
---------------------------
* sqlite에 깨진채로 저장된 shift_jis encoding 복구 불가능 함.
* json으로 bms list들을 받아올 수 있도록 만들 예정.
* 모바일 전용 지원 예정.


유의사항
--------
* 이 프로그램은 django와 bmx2wav, bootstrap, jquery를 내부적으로 이용하고 있으며 이에 대한 저작권은 소유자에게 있습니다.
* 이 프로그램은 MIT License를 따릅니다.