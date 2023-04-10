function openPanelver2(ht_name,sim,sim_id,sc,pick,seoul) {
  const panel = document.querySelector('.panel');
  console.log(panel);
  const panelContent = document.querySelector('.panel-content');

  panel.style.right = '0';
  panelContent.innerHTML = `
  <p align='center' style='font-size:12px';>${ht_name}</p>  
  <canvas id="MyChart" width="200" height="200"></canvas>
  <p align='center'> 유사 호텔 추천 </p>
  <table class='paneltable'>
  <thead>    
  </thead>
  <tbody>
    <tr>
      <td class='paneltd'>${sim.split('<br>')[0]}</td>
      <td class='paneltd'>
        <form action="/hotel" method="get" target="_blank">
          <input type="hidden" name="ht_id" value="${sim_id.split(',')[0].split('[')[1]}">
          <input type="hidden" name="ht_name" value="${sim.split('<br>')[0]}">
          <button type="submit">더 보기</button>
        </form>
      </td>
    </tr>
    <tr>
      <td class='paneltd'>${sim.split('<br>')[1]}</td>
      <td class='paneltd'>
        <form action="/hotel" method="get" target="_blank">
          <input type="hidden" name="ht_id" value="${sim_id.split(', ')[1]}">
          <input type="hidden" name="ht_name" value="${sim.split('<br>')[1]}">
          <button type="submit">더 보기</button>
        </form>
      </td>
    </tr>
    <tr>
      <td class='paneltd'>${sim.split('<br>')[2]}</td>
      <td class='paneltd'>
        <form action="/hotel" method="get" target="_blank">
          <input type="hidden" name="ht_id" value="${sim_id.split(', ')[2]}">
          <input type="hidden" name="ht_name" value="${sim.split('<br>')[2]}">
          <button type="submit">더 보기</button>
        </form>
      </td>
    </tr>
    <tr>
      <td class='paneltd'>${sim.split('<br>')[3]}</td>
      <td class='paneltd'>
        <form action="/hotel" method="get" target="_blank">
          <input type="hidden" name="ht_id" value="${sim_id.split(', ')[3]}">
          <input type="hidden" name="ht_name" value="${sim.split('<br>')[3]}">
          <button type="submit">더 보기</button>
        </form>
      </td>
    </tr>
    <tr>
      <td class='paneltd'>${sim.split('<br>')[4]}</td>
      <td class='paneltd'>
        <form action="/hotel" method="get" target="_blank">
          <input type="hidden" name="ht_id" value="${sim_id.split(', ')[4].split(']')[0]}">
          <input type="hidden" name="ht_name" value="${sim.split('<br>')[4]}">
          <button type="submit">더 보기</button>
        </form>
      </td>
    </tr>
  </tbody>
</table>


  `;
  panel.classList.add('open');

  const chardata = {
    "labels": ['가성비', '친절', '청결', '주변시설', '주차', '조식', '방음', '위치', '비품', '시설'],
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