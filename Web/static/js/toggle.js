var navbar = document.getElementById("navbar");
navbar.style.display = "none"
function displayBar() {
    if (navbar.style.display === "none") {
        navbar.style.display = "block"; // 显示导航栏
        navbar.style.height = "0"; // 设置起始高度为0
        navbar.style.transition = "height 0.5s ease"; // 添加过渡效果
        setTimeout(function () {
            navbar.style.height = "100%"; // 设置最终高度
        }, 10); // 延迟一点时间执行动画，确保过渡效果生效
    } else {
        navbar.style.height = "0"; // 设置高度为0
        setTimeout(function () {
            navbar.style.display = "none"; // 隐藏导航栏
        }, 300); // 等待过渡效果结束后隐藏导航栏
    }
}