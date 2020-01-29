
d3.csv("assets/data/apps_country.csv").then(d => stackedBarChart(d, "#chartCountries", 3, "month"));
d3.csv("assets/data/apps_top.csv").then(d => stackedBarChart(d, "#chartTops", 5, "month", "top"));
d3.csv("assets/data/apps_top.csv").then(d => stackedBarChart(d, "#chartCustomCat", 5, "month", "top"));

/**
 * Function that creates a Stacked Bar Chart According to information stored in a 
 * CSV file.
 * 
 * @param {*} csv Path and Name of the CSV file containing the information.
 * @param {*} chartId Identifier of the SVG tag
 * @param {*} filterAttr Name of the filtering attribute inside the CSV file
 * @param {*} groupAttr Name of the Grouping Attribute in the CSV file
 */
function stackedBarChart(csv, chartId, legendColumns, groupAttr, filterAttr=null) {
	const selectId = chartId + "xaxis";
	const sortId = chartId + "sort";
	const groupingValues = [...new Set(csv.map(d => d[groupAttr]))];
  
  /*Selecciona las columnas a utilizar para generar las barras*/
  var keys = csv.columns.filter(col => col !== filterAttr && col !== groupAttr);
  
	/*Adiciona las opciones () de agruacion para la generacion de la grafica*/
	if(filterAttr !== null) {
		var filteringValues   = [...new Set(csv.map(d => d[filterAttr]))];
		d3.select(selectId).selectAll("option")
			.data(filteringValues).enter().append("option").text(d => d);
	}
  
	var svg = d3.select(chartId),
		margin = {top: 35, left: 35, bottom: 0, right: 0},
		width = +svg.attr("width") - margin.left - margin.right,
		height = (+svg.attr("height") - margin.top - margin.bottom) * 0.75;
	
  var div = d3.select("body").append("div")	
    .attr("class", "tooltip")				
		.style("opacity", 0)
		.style("display", "none");
  
	var x = d3.scaleBand()
		.range([margin.left, width - margin.right])
		.padding(0.1)

	var y = d3.scaleLinear()
		.rangeRound([height - margin.bottom, margin.top])

	var xAxis = svg.append("g")
		.attr("transform", `translate(0,${height - margin.bottom})`)
		.attr("class", "x-axis")

	var yAxis = svg.append("g")
		.attr("transform", `translate(${margin.left},0)`)
		.attr("class", "y-axis")
  
	var color = d3.scaleOrdinal()
		.range(d3.schemeSet2.concat(d3.schemeSet3) )
		.domain(keys);
  
  var legend = svg.selectAll("legend").data(keys)
		.enter().append("circle")
  	.attr("cx", (d,i) => 40 + ((width * 0.95) / legendColumns) * (i%legendColumns)  )
  	.attr("cy", (d,i) => (height + margin.top) + (20 * Math.floor(i/legendColumns)) )
  	.attr("r", 7)
  	.style("fill",  d => color(d));

	var labels = svg.selectAll("mylegend").data(keys)
  .enter().append("text")
    .attr("x", (d,i) => 50 + ((width * 0.95) / legendColumns) * (i%legendColumns)  )
  	.attr("y", (d,i) => (height + margin.top) + (20 * Math.floor(i/legendColumns)) )
    .attr("fill",  d => color(d))
    .text(d => d.split(" ")[0].length > 12 ? d.slice(0,9) + "..." : d.split(" ")[0])
    .attr("text-anchor", "left")
    .style("alignment-baseline", "middle")
  	.on("mouseover", (d) => mouseOver(d, d))
  	.on("mousemove", mouseMove)
  	.on("mouseout", mouseOut);

	update(filterAttr !== null? d3.select(selectId).property("value") : null);
  
  /**
   * Updates de information of the graph/chart depending on external inputs an user actions
   * 
   * @param {*} input Value used to filter the data that will be used in the graph
   * @param {*} speed Transition time (milliseconds) of the update.
   */
	function update(input, speed=0) {
		var data = csv.filter(f => input === null || f[filterAttr] === input)

		data.forEach(function(d) {
			d.total = d3.sum(keys, k => +d[k])
			return d;
		});

		y.domain([0, d3.max(data, d => d3.sum(keys, k => +d[k]))]).nice();

		svg.selectAll(".y-axis").transition().duration(speed)
			.call(d3.axisLeft(y).ticks(null, "s"))

		data.sort(d3.select(sortId).property("checked")
			? (a, b) => b.total - a.total
			: (a, b) => groupingValues.indexOf(a.State) - groupingValues.indexOf(b.State))
		
		x.domain(data.map(d => d[groupAttr]));

		svg.selectAll(".x-axis").transition().duration(speed)
			.call(d3.axisBottom(x).tickSizeOuter(0))

		var group = svg.selectAll("g.layer")
			.data(d3.stack().keys(keys)(data), d => d.key)

		group.exit().remove()

		group.enter().append("g")
			.classed("layer", true)
			.attr("fill", d => color(d.key));

		var bars = svg.selectAll("g.layer").selectAll("rect")
			.data(d => d, e => e.data[groupAttr]);

		bars.exit().remove()

		bars.enter().append("rect")
			.attr("width", x.bandwidth())
    	.on("mouseover", function(d) {
        var subgroupName = d3.select(this.parentNode).datum().key;
        var subgroupValue = d.data[subgroupName];
        mouseOver(d, subgroupName + "<br/>" + subgroupValue + " Apps");
      }).on("mousemove", mouseMove)
      .on("mouseout", mouseOut)
			.merge(bars)
		.transition().duration(speed)
			.attr("x", d => x(d.data[groupAttr]))
			.attr("y", d => y(d[1]))
			.attr("height", d => y(d[0]) - y(d[1]))
    

		var text = svg.selectAll(".text")
			.data(data, d => d[groupAttr]);

		text.exit().remove()

		text.enter().append("text")
			.attr("class", "text")
			.attr("text-anchor", "middle")
			.merge(text)
		.transition().duration(speed)
			.attr("x", d => x(d[groupAttr]) + x.bandwidth() / 2)
			.attr("y", d => y(d.total) - 5)
			.text(d => d.total)
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
   * Updates de position of the activated Tooltip according to the position of the mouse
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
  
  /**
   * Directive that updates the graph whenever there's a change in the sorting input
   */
	var checkbox = d3.select(sortId)
		.on("click", function() {
			update(filterAttr !== null? select.property("value") : null, 750)
		});
};
