 // 전체 체크박스와 다른 체크박스를 가져옵니다.
 var allCheckbox = document.getElementsByName('level')[0];
 var checkboxes = document.getElementsByName('level_checkbox');

 // 체크박스 전체 선택/해제 함수
 function checkAll(checked) {
   allCheckbox.checked = checked;
   for (var i = 0; i < checkboxes.length; i++) {
     checkboxes[i].checked = checked;
   }
 }

 // 전체 체크박스의 상태가 변경되면 다른 체크박스들의 상태도 변경
 allCheckbox.addEventListener('change', function() {
   checkAll(this.checked);
 });

 // 다른 체크박스를 선택/해제할 때 전체 체크박스의 상태를 동적으로 변경
 function updateAllCheckbox() {
   var allChecked = true;
   for (var i = 0; i < checkboxes.length; i++) {
     if (!checkboxes[i].checked) {
       allChecked = false;
       break;
     }
   }
   allCheckbox.checked = allChecked;
 }