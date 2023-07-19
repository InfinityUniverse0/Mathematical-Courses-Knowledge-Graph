// 模拟的查询结果数据，用于示例
    var courses = [
        { name: '高等代数 II', description: '让学生加深对线性代数的理解，能够把上学期学过的具体概念，演算应用到跟一般的线性空间，线性变换，双线性函数，同时能利用抽象的线性空间，线性变换，双线性函数等概念来解决具体的问题。', textbook: '北京大学数学力学系几何与代数教研室代数小组：高等代数，高等教育出版社，1984（第6 次印刷）。|蓝以中：高等代数简明教程（上册），北京大学出版社，2003（第 2 次印刷）。|丘维声：高等代数（第二版）上册，高等教育出版社，2002 年。' },
        { name: '课程1', description: '课程2介绍', textbook: '教材2' },
        { name: '课程1', description: '课程3介绍', textbook: '教材3' },
        { name: '课程1', description: '课程4介绍', textbook: '教材4' },
        { name: '课程1', description: '课程5介绍', textbook: '教材5' }
    ];

    var currentPage = 1;
    var coursesPerPage = 1; // 每页显示的课程数量

    function displayCourses() {
        var input1 = document.querySelector('.entityInput1');
        //var input2 = document.querySelector('.entityInput2');
        var keyword1 = input1.value;
        //var keyword2 = input2.value;
        var filteredCourses = [];

        if (keyword1 !== '') {
            // 根据课程关键字查询课程
            filteredCourses = courses.filter(function (course) {
                return course.name.toLowerCase().includes(keyword1.toLowerCase());
            });
        }
//        else if (keyword2 !== '') {
//            // 根据数学知识点查询课程
//            filteredCourses = courses.filter(function (course) {
//                return course.description.toLowerCase().includes(keyword2.toLowerCase());
//            });
//        }

        // 更新表格数据
        var courseData = document.getElementsByClassName('courseData')[0];
        courseData.innerHTML = '';

        if (filteredCourses.length > 0) {
            // 计算当前页起始和结束索引
            var startIndex = (currentPage - 1) * coursesPerPage;
            var endIndex = startIndex + coursesPerPage;

            // 循环添加当前页的课程数据
            for (var i = startIndex; i < endIndex && i < filteredCourses.length; i++) {
                var course = filteredCourses[i];
                var row = document.createElement('tr');
                var nameCell = document.createElement('td');
                var descriptionCell = document.createElement('td');
                var textbookCell = document.createElement('td');

                nameCell.textContent = course.name;
                descriptionCell.textContent = course.description;
                textbookCell.textContent = course.textbook;

                row.appendChild(nameCell);
                row.appendChild(descriptionCell);
                row.appendChild(textbookCell);

                courseData.appendChild(row);
            }

            // 更新分页按钮状态
            var pagination = document.querySelector('.pagination');
            pagination.style.display = 'block';
            var previousButton = pagination.querySelector('button:first-child');
            var nextButton = pagination.querySelector('button:last-child');
            var pageInfo = document.getElementById('pageInfo');
            pageInfo.textContent = currentPage + '/' + Math.ceil(filteredCourses.length / coursesPerPage);

            if (currentPage === 1) {
                previousButton.disabled = true;
            } else {
                previousButton.disabled = false;
            }

            if (endIndex >= filteredCourses.length) {
                nextButton.disabled = true;
            } else {
                nextButton.disabled = false;
            }
        }
//        else {
//            // 如果没有查询到课程，隐藏分页按钮
//            var pagination = document.querySelector('.pagination');
//            pagination.style.display = 'none';
//        }
    }

    function previousPage() {
        if (currentPage > 1) {
            currentPage--;
            displayCourses();
        }
    }

    function nextPage() {
        var input1 = document.querySelector('.entityInput1');
        //var input2 = document.querySelector('.entityInput2');
        var keyword1 = input1.value;
        //var keyword2 = input2.value;
        var filteredCourses = [];

        if (keyword1 !== '') {
            // 根据课程关键字查询课程
            filteredCourses = courses.filter(function (course) {
                return course.name.toLowerCase().includes(keyword1.toLowerCase());
            });
        }
//        else if (keyword2 !== '') {
//            // 根据数学知识点查询课程
//            filteredCourses = courses.filter(function (course) {
//                return course.description.toLowerCase().includes(keyword2.toLowerCase());
//            });
//        }

        // 计算当前页起始和结束索引
        var startIndex = currentPage * coursesPerPage;
        var endIndex = startIndex + coursesPerPage;

        if (endIndex <= filteredCourses.length) {
            currentPage++;
            displayCourses();
        }
    }