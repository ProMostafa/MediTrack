import React from 'react';
import Chart from 'react-apexcharts';

const BarChart = ({ series, title, categories }) => {
  const options = {
    chart: {
      type: 'bar',
      height: 400,
    },
    plotOptions: {
      bar: {
        horizontal: false,
        endingShape: 'rounded',
      },
    },
    dataLabels: {
      enabled: true,
    },
    colors: ['#3498db', '#e74c3c', '#2ecc71'],
    xaxis: {
      categories: categories,
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
        },
      },
    ],
  };

  return (
    <div className="chart-container">
      <Chart options={options} series={series} type="bar" height={400} />
    </div>
  );
};

export default BarChart;
