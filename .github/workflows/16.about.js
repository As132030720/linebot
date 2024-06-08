window.onload=function(){
  var items=document.getElementsByClassName("item");
  var circles=document.getElementsByClassName("circle");
  var leftBtn=document.getElementById("btn-left");
  var rightBtn=document.getElementById("btn-right");
  var content=document.querySelector('.content');
  var index=0;
  var timer=null;
   
  //清除class
  var clearclass=function(){
   for(let i=0;i<items.length;i++){
    items[i].className="item";
    circles[i].className="circle";
    circles[i].setAttribute("num",i);
   }
  }
  /*只顯示一个class*/
  function move(){
   clearclass();
   items[index].className="item active";
   circles[index].className="circle white";
  }
  //右邊按鈕
  rightBtn.onclick=function(){
   if(index<items.length-1){
    index++;
   }
   else{
    index=0;
   }
   move();
  }
  //左邊按鈕
  leftBtn.onclick=function(){
   if(index<items.length){
    index--;
   }
   else{
    index=items.length-1;
   }
   move();
  }
  //輪播定時器
  timer=setInterval(function(){
   rightBtn.onclick();
  },1500)
  //點圓點跳相對應圖片
  for(var i=0;i<circles.length;i++){
   circles[i].addEventListener("click",function(){
    var point_index=this.getAttribute("num");
    index=point_index;
    move();
   })
   
  }
  //滑鼠進入，更改為3秒定時器
  content.onmouseover=function(){
   clearInterval(timer);
    timer=setInterval(function(){
     rightBtn.onclick();
    },3000)
  }
  //滑鼠離開：開定時器
  content.onmouseleave=function(){
   clearInterval(timer);
   timer=setInterval(function(){
    rightBtn.onclick();
   },1500)
  }
  }