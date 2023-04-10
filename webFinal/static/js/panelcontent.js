function openPanelver2(ht_name,sc,pick,seoul) {
  const panel = document.querySelector('.panel');
  console.log(panel);
  const panelContent = document.querySelector('.panel-content');

  panel.style.right = '0';
  panelContent.innerHTML = `
  <p align='center' style='font-size:19px';><strong>${ht_name}</strong></p>  
  <div style="margin-top: 50px">
  <canvas id="MyChart" width="200" height="200"  ></canvas>
  </div>


  `;
  panel.classList.add('open');

  const chardata = {
    "labels": ['가성비', '친절', '청결', '관광', '주차', '조식', '방음', '교통', '비품', '시설'],
    "datasets": [
        {
            "label": ht_name,
            "data": sc,
            "fill": true,
            "backgroundColor": "rgba(255, 99, 132, 0.2)",
            "borderColor": "rgba(255, 99, 132, 1)",
            "pointBackgroundColor": "rgba(255, 99, 132, 1)",
            "pointBorderColor": "#fff",
            "pointHoverBackgroundColor": "#fff",
            "pointHoverBorderColor": "rgba(255, 99, 132, 1)"
        },
        {  "label": "서울평균",
          "data": seoul,
          "fill": true,
          "backgroundColor": "rgba(54, 162, 235, 0.2)",
          "borderColor": "rgba(54, 162, 235, 1)",
          "pointBackgroundColor": "rgba(54, 162, 235, 1)",
          "pointBorderColor": "#fff",
          "pointHoverBackgroundColor": "#fff",
          "pointHoverBorderColor": "rgba(54, 162, 235, 1)"
      },
      {"label": "추천평균",
      "data": pick,
      "fill": true,
      "backgroundColor": "rgba(55,116,72, 0.2)",
      "borderColor": "rgba(55,116,72, 1)",
      "pointBackgroundColor": "rgba(55,116,72, 1)",
      "pointBorderColor": "#fff",
      "pointHoverBackgroundColor": "#fff",
      "pointHoverBorderColor": "rgba(55,116,72, 1)"
    }
      ]
    };

    var canvas = document.getElementById('MyChart');
    canvas.style.width = '200px';
    canvas.style.height = '200px';
    
    var data = chardata;
    var chart = new Chart(canvas, {
      type: 'radar',  
      data: data,
      options: {
        scales: {
          yAxes: [{
          ticks: {
            callback: function() {
              return '$';
            }
          }
        }]
        }
      }
    });
}

  function closePanel() {
    const panel = document.querySelector('.panel');
    panel.classList.remove('open');
  }