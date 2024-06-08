// 等待DOM内容加载完成
document.addEventListener('DOMContentLoaded', function() {
    // 获取 reservation 表单元素的父元素 ( .reservation )
    const reservationContainer = document.querySelector('.reservation');

    // 鼠标进入表单时，设置背景颜色为绿色
    reservationContainer.addEventListener('mouseenter', function() {
        reservationContainer.style.transition = 'background-color 0.5s ease'; // 进入过渡效果
        reservationContainer.style.backgroundColor = 'green';
    });

    // 鼠标离开表单时，逐渐恢复原来的背景颜色
    reservationContainer.addEventListener('mouseleave', function() {
        // 添加类名以触发背景逐渐恢复的效果
        reservationContainer.classList.add('mouse-out');

        // 等待过渡效果生效后，移除类名
        setTimeout(function() {
            reservationContainer.classList.remove('mouse-out');
        }, 1000); // 1秒后移除类名
    });
});
// 当页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 获取表单元素
    const reservationForm = document.querySelector('.reservation');

    // 监听鼠标离开事件
    reservationForm.addEventListener('mouseleave', function() {
        // 将表单的背景颜色设置为橘色
        reservationForm.style.backgroundColor = '#186eeef8';
    });
});

