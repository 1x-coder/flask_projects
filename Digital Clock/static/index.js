setInterval(() => {
    let a = new Date()
    let time = a.getHours() + " : " + a.getMinutes() + " : " + a.getSeconds();
    if (a.getHours() >= 12) {
        document.getElementById('time').innerHTML = time + " PM";
    } else {
        document.getElementById('time').innerHTML = time + "AM";
    }

}, 1000);

setInterval(() => {
    let b = new Date()
    var weekday = new Array(7);
    weekday[0] = "SUNDAY";
    weekday[1] = "MONDAY";
    weekday[2] = "TUESDAY";
    weekday[3] = "WEDNESDAY";
    weekday[4] = "THURSDAY";
    weekday[5] = "FRIDAY";
    weekday[6] = "SATURDAY";

    var n = weekday[b.getDay()];
    document.getElementById('day').innerHTML = n;
}, 1000);

setInterval(() => {
    let c = new Date()
    let date = c.toLocaleDateString();
    document.getElementById('date').innerHTML = date;
}, 1000);