d3.csv("assets/data/mongo_app.csv").then(d => pieChart(d, "#chartTypesApp", 4, "country"));
// d3.csv("database_types.csv").then(d => pieChart(d, "#chartTypesReview", 4, "country"));
// d3.csv("database_types.csv").then(d => pieChart(d, "#chartTypesExtra", 4, "country"));

/**
 * Function that creates a Stacked Bar Chart According to information stored in a 
 * CSV file.
 * 
 * @param {*} csv Path and Name of the CSV file containing the information.
 * @param {*} chartId Identifier of the SVG tag
 * @param {*} labelCols Number of columns in the legend
 * @param {*} filterAttr Name of the filtering attribute inside the CSV file
 */
function pieChart(csv, chartId, labelCols, filterAttr=null) {
  const selectId = chartId + "xaxis";
  const keys = [...new Set(csv.map(d => d.label))];

  /*Adiciona las opciones () de agruacion para la generacion de la grafica*/
  if(filterAttr !== null) {
    var filteringValues = [...new Set(csv.map(d => d[filterAttr]))];
    d3.select(selectId).selectAll("option").data(filteringValues)
      .enter().append("option").text(d => d);
  }

  var svg = d3.select(chartId),
    margin = {top: 35, left: 35, bottom: 0, right: 0},
    width = +svg.attr("width") - margin.left - margin.right,
    height = (+svg.attr("height") - margin.top - margin.bottom) * 0.75,
    radius = Math.min(width, height) / 2;
  
  var div = d3.select("body").append("div")	
    .attr("class", "tooltip")				
    .style("opacity", 0)
    .style("display", "none");

  var color = d3.scaleOrdinal( )
    .range(d3.schemeSet2.concat(d3.schemeSet3))
    .domain(keys);

  var pie = d3.pie()
    .value(function(d) { return d.value; })
    .sort(null);
  
  var arc = d3.arc()
    .innerRadius(radius - 65)
    .outerRadius(radius);
  
  var svg = svg.append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");;
  
  var path = svg.datum(csv).selectAll("path").data(pie)
    .enter().append("path")
    .attr("fill", function(d, i) {return color(d.data.label); })
    .attr("d", arc)
    .on("mouseover", function(d) {
      mouseOver(d, d.data.label + ": " + d.data.value + "%");
    })
    .on("mousemove", mouseMove)
    .on("mouseout", mouseOut)
    .each(function(d) { this._current = d; }); 
  
  var legend = d3.select(chartId).selectAll("legend").data(keys)
    .enter().append("circle")
    .attr("cx", (d,i) => 40 + ((width * 0.95) / labelCols) * (i%labelCols)  )
    .attr("cy", (d,i) => (height + margin.top) + (20 * Math.floor(i/labelCols)) )
    .attr("r", 7)
    .style("fill",  d => {return color(d)});

  var labels = d3.select(chartId).selectAll("mylegend").data(keys)
  .enter().append("text")
    .attr("x", (d,i) => 50 + ((width * 0.95) / labelCols) * (i%labelCols)  )
    .attr("y", (d,i) => (height + margin.top) + (20 * Math.floor(i/labelCols)) )
    .attr("fill",  d => color(d))
    .text(d =>  {console.log(d); return d.length > 12 ? d.slice(0,9) + "..." : d})
    .attr("text-anchor", "left")
    .style("alignment-baseline", "middle")
    .on("mouseover", (d) => mouseOver(d, d))
    .on("mousemove", mouseMove)
    .on("mouseout", mouseOut);
  
  
  update(filterAttr !== null? d3.select(selectId).property("value") : null);

  /**
   * Updates de information of the graph/chart depending on external inputs
   * 
   * @param {*} input Value used to filter the data that will be used in the graph
   * @param {*} speed Transition time (milliseconds) of the update.
   */ 
  function update(input, speed=0) {      
    var data = csv.filter(f => input === null || f[filterAttr] === input);
    pie.value(function(d){ return d[filterAttr] === input ? d.value: 0;}); 
    path = path.data(pie);
    path.transition().duration(750).attrTween("d", arcTween);
  };
  
  function arcTween(a) {
    var i = d3.interpolate(this._current, a);
    this._current = i(0);
    return function(t) {
      return arc(i(t));
    };
  }

  /**
   * Activates a Tooltip component to show detail information of the graph's components
   * 
   * @param {*} d Node or component of the graph
   * @param {*} message Information of the Node that will be displayed in the Tooltip
   */
  function mouseOver(d, message) {
    div.transition().duration(200)
      .style("opacity", .9)
      .style("display", "inline");
    div.html(message);
  }

  /**
   * Updates de position of the activated Tooltip according to the 
     position of the mouse
    * @param {*} d Node or component of the graph
    */
  function mouseMove(d) {
    div.style("left", (d3.event.pageX - 34) + "px")
      .style("top", (d3.event.pageY - 12) + "px");
  }

  /**
   * Deactivates the Tooltip component 
   * @param {*} d Node or component of the graph
   */
  function mouseOut(d) {
    div.transition().duration(500)
      .style("opacity", 0)
      .style("display", "none");
  }

  /**
   * Directive that updates the graph whenever there's a change in the filtering input
   */
  var select = filterAttr === null? null : d3.select(selectId)
    .on("change", function() {
      update(this.value, 750)
    });
};