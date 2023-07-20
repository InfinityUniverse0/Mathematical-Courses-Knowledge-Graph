var currentPage = 1;
var coursesPerPage = 1; // 每页显示的课程数量
/* 产生查询课程的异步请求 */
function sendCourseRequest(post, inputValue) {
    fetch(post, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache'
        },
        body: JSON.stringify({
            name: inputValue
        })
    })
        .then(response => response.json())
        .then(data => {
            setCourseData(data.search)
        })
        .catch(error => {
            console.log('请求失败:', error);
        });
}

function sendKnowRequest(post, inputValue) {
    fetch(post, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache'
        },
        body: JSON.stringify({
            name: inputValue
        })
    })
        .then(response => response.json())
        .then(data => {
            setKnowData(data.search)
        })
        .catch(error => {
            console.log('请求失败:', error);
        });
}

function setCourseData(Data) {
    if (Data) {
        data_string = Data.nodes;
        data_courses = JSON.parse(data_string);
        /*对数据进行清洗，筛选出课程节点，同时根据id键去重*/
        if (data_courses) {
            var idSet = new Set();
            courses = data_courses.filter(function (item) {
                if ('refer' in item && !idSet.has(item.id)) {
                    idSet.add(item.id);
                    return true;
                }
                return false;
            });
        }
        currentPage = 1; // 将当前页设置为1
        sendRequest('post3', courses[0].name)
        displayCourses(courses);
    }
    /* 若查询不到信息，则清空当前表格 */
    else {
        // 清空表格数据
        var courseData = document.getElementsByClassName('courseData')[0];
        courseData.innerHTML = '';
        // 隐藏分页按钮
        var pagination = document.querySelector('.pagination');
        pagination.style.display = 'none';
    }
}

function setKnowData(Data) {
    if (Data) {
        if (Data.point) {
            kn_points = Data.point;
        } else {
            var knData0 = document.getElementsByClassName('fuzzData')[0];
            knData0.innerHTML = '';
        }
        if (Data.module) {
            kn_modules = Data.module;
        } else {
            var knData1 = document.getElementsByClassName('fuzzData')[1];
            knData1.innerHTML = '';
        }
        if (Data.course) {
            kn_courses = Data.course;
        } else {
            var knData2 = document.getElementsByClassName('fuzzData')[2];
            knData2.innerHTML = '';
        }
        console.log(kn_points[0]);
        //    console.log(kn_modules);
        //    console.log(kn_courses);
        displayknpoint(kn_points, kn_modules, kn_courses);
    }
}


function displayCourses(Courses, callback) {
    // 更新表格数据
    var courseData = document.getElementsByClassName('courseData')[0];
    courseData.innerHTML = '';
    if (Courses.length > 0) {
        // 计算当前页起始和结束索引
        var startIndex = (currentPage - 1) * coursesPerPage;
        var endIndex = startIndex + coursesPerPage;

        // 循环添加当前页的课程数据
        for (var i = startIndex; i < endIndex && i < Courses.length; i++) {
            var course = Courses[i];
            var row = document.createElement('tr');
            var nameCell = document.createElement('td');
            var descriptionCell = document.createElement('td');
            var textbookCell = document.createElement('td');

            nameCell.textContent = course.name;
            descriptionCell.textContent = course.intro;
            textbookCell.textContent = course.refer;

            row.appendChild(nameCell);
            row.appendChild(descriptionCell);
            row.appendChild(textbookCell);

            courseData.appendChild(row);
            /* 回调函数获取到当前表格的课程姓名 */
            if (typeof callback === 'function') {
                var courseName = course.name;
                callback(courseName);
            }
        }

        // 更新分页按钮状态
        var pagination = document.querySelector('.pagination');
        pagination.style.display = 'block';
        var previousButton = pagination.querySelector('button:first-child');
        var nextButton = pagination.querySelector('button:last-child');
        var pageInfo = document.getElementById('pageInfo');
        pageInfo.textContent = currentPage + '/' + Math.ceil(Courses.length / coursesPerPage);

        if (currentPage === 1) {
            previousButton.disabled = true;
        } else {
            previousButton.disabled = false;
        }

        if (endIndex >= Courses.length) {
            nextButton.disabled = true;
        } else {
            nextButton.disabled = false;
        }
    }
}

function displayknpoint(kn_points, kn_modules, kn_courses) {
    // 更新知识要点表格数据
    var knData0 = document.getElementsByClassName('fuzzData')[0];
    knData0.innerHTML = '';

    if (kn_points.length > 0) {
        // 循环添加当前知识要点
        for (var i = 0; i < kn_points.length; i++) {
            var point = kn_points[i];
            var row = document.createElement('tr');
            var pointCell = document.createElement('td');
            pointCell.textContent = point;
            row.appendChild(pointCell);
            knData0.appendChild(row);
        }
    }

    // 更新知识模块表格数据
    var knData1 = document.getElementsByClassName('fuzzData')[1];
    knData1.innerHTML = '';

    if (kn_modules.length > 0) {
        // 循环添加当前知识要点
        for (var i = 0; i < kn_modules.length; i++) {
            var module = kn_modules[i];
            var row = document.createElement('tr');
            var moduleCell = document.createElement('td');
            moduleCell.textContent = module;
            row.appendChild(moduleCell);
            knData1.appendChild(row);
        }
    }

    // 更新知识课程表格数据
    var knData2 = document.getElementsByClassName('fuzzData')[2];
    knData2.innerHTML = '';

    if (kn_courses.length > 0) {
        // 循环添加当前知识要点
        for (var i = 0; i < kn_courses.length; i++) {
            var course = kn_courses[i];
            var row = document.createElement('tr');
            var courseCell = document.createElement('td');
            courseCell.textContent = course;
            row.appendChild(courseCell);
            knData2.appendChild(row);
        }
    }
}

function previousPage() {
    if (currentPage > 1) {
        currentPage--;
        /*调用回调函数，显示当前courseName*/
        displayCourses(courses, handleCourseNames);
    }
}

function nextPage() {
    var startIndex = currentPage * coursesPerPage;
    var endIndex = startIndex + coursesPerPage;
    if (endIndex <= courses.length) {
        currentPage++;
        /*调用回调函数，显示当前courseName*/
        displayCourses(courses, handleCourseNames);
    }
}