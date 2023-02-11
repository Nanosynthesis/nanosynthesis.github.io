window.onload=function ()
{
	var oDiv=document.getElementById("banner");
	var imgLeft=getByClass(oDiv, "imgLeft")[0];
	var imgList=getByClass(oDiv, "imgList")[0];
	var imgArr=imgList.getElementsByTagName("li");
	
	
	//鼠标放在左右翻页及图片上时,左右翻页透明度变为100
	oDiv.onmouseover=function ()
	{
		startMove(imgLeft, 'opacity', 100);
	};
	//鼠标移出图片时,左右翻页透明度变为0
	oDiv.onmouseout=function ()
	{
		startMove(imgLeft, 'opacity', 0);
	};
	
	
	imgList.style.width=6*800+"px";
	
	var index = 0;
	var timer;
	
	function autoChange(){
		
		//开启一个定时器，用来定时去切换图片
		timer = setInterval(function(){
			index++;
			
			//判断index的值
			if(index>=imgArr.length){
				imgList.style.left=0+"px";
				index=0;
			}
			
			//执行动画，切换图片
			move(imgList , "left" , -800*index , 20 , null);
			
		},5000);
		
	}
	autoChange();
	
	imgLeft.onclick=function(){
		index--;
		clearInterval(timer);
			if(index==-1)
			{
				index=imgArr.length-2;
			}
		imgList.style.left=-800*index+"px";
		autoChange();
	}
}
