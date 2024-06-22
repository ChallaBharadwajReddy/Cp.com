self.onmessage = function(e){
    let time=e.data;
    setInterval(()=>{
        time--;
        self.postMessage(time);
    },1000)
}