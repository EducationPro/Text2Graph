function init() {
		var _ = go.GraphObject.make; // for conciseness in defining templates

		myDiagram =
				_(go.Diagram, "myDiagramDiv", // must name or refer to the DIV HTML element
						{
								initialAutoScale: go.Diagram.Uniform, // an initial automatic zoom-to-fit
								contentAlignment: go.Spot.Center, // align document to the center of the viewport
								layout: _(go.ForceDirectedLayout, // automatically spread nodes apart
										{
												maxIterations: 200,
												defaultSpringLength: 30,
												defaultElectricalCharge: 100
										})
						});

		// define each Node's appearance
		myDiagram.nodeTemplate =
				_(go.Node, "Auto", // the whole node panel
						{
								locationSpot: go.Spot.Center
						},
						// define the node's outer shape, which will surround the TextBlock
						_(go.Shape, "Rectangle", {
								fill: _(go.Brush, "Linear", {
										0: "rgb(254, 201, 0)",
										1: "rgb(254, 162, 0)"
								}),
								stroke: "black"
						}),
						_(go.TextBlock, {
										font: "bold 15pt helvetica, bold arial, sans-serif",
										margin: 4
								},
								new go.Binding("text", "text"))
				);

		// replace the default Link template in the linkTemplateMap
		myDiagram.linkTemplate =
				_(go.Link, // the whole link panel
						_(go.Shape, // the link shape
								{
										stroke: "black"
								}),
						_(go.Shape, // the arrowhead
								{
										toArrow: "standard",
										stroke: null
								}),
						_(go.Panel, "Auto",
								_(go.Shape, // the label background, which becomes transparent around the edges
										{
												fill: _(go.Brush, "Radial", {
														0: "rgb(240, 240, 240)",
														0.3: "rgb(240, 240, 240)",
														1: "rgba(240, 240, 240, 0)"
												}),
												stroke: null
										}),
								_(go.TextBlock, // the label text
										{
												textAlign: "center",
												font: "15pt helvetica, arial, sans-serif",
												stroke: "#555555",
												margin: 4
										},
										new go.Binding("text", "text"))
						)
				);

		// create the model for the concept map
		var nodeDataArray = [];
		var linkDataArray = [];
		window.tree = [];
		$('#spinner').addClass('fa-spin');
		var request = $.ajax({
				xhrFields: {
						withCredentials: true
				},
				dataType: 'json',
				async: false,
				method: 'GET',
				url: "/api/v1.1/text/answer/",
				data: {
						text: 'Google is a high-tech company.',
						question: 'What is Google?'
				}
		});

		request.done(function(data) {
				console.log(data);
				window.tree = [data];
				$('#spinner').removeClass('fa-spin');
		});
		request.fail(function(ajaxContext) {
				console.log(ajaxContext.responseText);
				//alert(ajaxContext.responseText);
				window.tree = [JSON.parse (ajaxContext.responseText)];
				$('#spinner').removeClass('fa-spin');
		});

		function dfs(node) {
				console.log(node);
				if (Array.isArray(node)) {
						let id = [];
						for (const x of node) {
								for (const y of dfs(x)) {
										id.push(y);
								}
						}
						return id;
				} else {
						let current_id = nodeDataArray.length;
						let label = '';

						for (const prop of node['properties']) {
								label = label + prop + '\n';
						}
						label = label.substring(0, label.length - 1);
						nodeDataArray.push({
								key: current_id,
								text: label
						});

						for (const action of node['actions']) {
								for (const obj of action['obj']) {
										let child_id = dfs(obj);
										for (const x of child_id) {
												linkDataArray.push({
														from: current_id,
														to: x,
														text: action['action']
												});
										}
								}
						}

						return [current_id];
				}
		}

		dfs(window.tree);

		myDiagram.model = new go.GraphLinksModel(nodeDataArray, linkDataArray);

		$('#submit').click(function(ev) {
				$('#spinner').addClass('fa-spin');

				var request = $.ajax({
						xhrFields: {
								withCredentials: true
						},
						dataType: 'json',
						async: false,
						method: 'GET',
						url: "/api/v1.1/text/answer/",
						data: {
								text: $('#text').val(),
								question: $('#question').val()
						}
				});

				request.done(function(data) {
						console.log(data);
						window.tree = [data];
						$('#spinner').removeClass('fa-spin');
				});

				request.fail(function(ajaxContext) {
						window.tree = [{"actions":[],"properties":["have","an","error"]}];
						$('#spinner').removeClass('fa-spin');
				});

				nodeDataArray = [];
				linkDataArray = [];
				dfs(window.tree);

				myDiagram.model = new go.GraphLinksModel(nodeDataArray, linkDataArray);
		});

		$("#text").val('Google is a high-tech company.');
		$("#question").val('What is Google?');
}
