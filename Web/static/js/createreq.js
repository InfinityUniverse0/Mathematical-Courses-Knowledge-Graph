/*function goToQuery() {
    // 使用 AJAX 请求获取query.html页面内容
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'info_query', true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            // 将获取到的内容插入到当前页面中
            document.body.innerHTML = xhr.responseText;
        }
    };
    xhr.send();
}*/
function goToQuery() {
    // 获取当前URL
    // var currentUrl = window.location.href;
    // 修改路径部分
    // var newUrl = currentUrl.substring(0, currentUrl.lastIndexOf("/") + 1) + "info_query";
    //console.log(newUrl)
    newUrl = "http://127.0.0.1:8000/kg/info_query/"
    // 跳转到新的URL（GET请求）
    window.location.href = newUrl;
}

function goToStudyRoute() {
    newUrl = "http://127.0.0.1:8000/kg/study_route/"
    // 跳转到新的URL（GET请求）
    window.location.href = newUrl;
}

function goToCoursesOverview() {
    newUrl = "http://127.0.0.1:8000/kg/courses_overview/"
    // 跳转到新的URL（GET请求）/
    window.location.href = newUrl;
}
function goToQuestionAnswer() {
    newUrl = "http://127.0.0.1:8000/qa/question_answer/"
    // 跳转到新的URL（GET请求）
    window.location.href = newUrl;
}