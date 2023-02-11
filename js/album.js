window.onload=function ()
{
	
	var album=document.getElementById("faculty");
	var facArr=faculty.getElementsByTagName("a");
	for(var i=0;i<facArr.length;i++)
	{
		facArr[i].onclick=function(){
			for(var j=0;j<facArr.length;j++)
			{
				facArr[j].style.backgroundColor="#EBEBEB";
			};
			this.style.backgroundColor="#11719E";
		}
	}
}