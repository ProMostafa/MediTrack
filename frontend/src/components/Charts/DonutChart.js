import React from 'react';
import Chart from 'react-apexcharts';

const DonutChart = ({ series, title, labels }) => {
  const options = {
    series: series,
    chart: {
      width: 380,
      type: 'donut',
    },
    plotOptions: {
      pie: {
        startAngle: -90,
        endAngle: 270,
      },
    },
    dataLabels: {
      enabled: false,
    },
    fill: {
      type: 'gradient',
    },
    colors: ['#3498db', '#e74c3c', '#2ecc71'],
    legend: {
      formatter: function (val, opts) {
        return `${labels[opts.seriesIndex]} - ${opts.w.globals.series[opts.seriesIndex]}`;
      },
    },
    title: {
      text: title || 'Default Title',
    },
    responsive: [
      {
        breakpoint: 480,
        options: {
          chart: {
            width: 200,
          },
          legend: {
            position: 'bottom',
          },
        },
      },
    ],
  };

  return (
    <div id="chart" className="chart-container">
      <Chart options={options} series={options.series} type="donut" width={380} />
    </div>
  );
};

export default DonutChart;
