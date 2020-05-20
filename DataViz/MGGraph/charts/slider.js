console.log("Original Data:")
console.log(source.data)
const data = source.data;
const t_slider = slider.value;

console.log("Time List:")
console.log(timeList[t_slider])

const t_hover = data['t_hover'];
const x = data['x']
const colors = data['colors']
const aux_color = data['aux_color']
const color_values = data['color_values']
const _timeList = timeList[t_slider];

for (var i = 0; i < t_hover.length; i++) {
    t_hover[i] = _timeList[i];
    r = (50 + 2 * aux_color[i]);
    r = r.toString(16);
    r = r.substring(0, 2);

    g = _timeList[i];
    g = (30 + 2 * (g / 100));
    g = g.toString(16);
    g = g.substring(0, 2);


    b = (150).toString(16);

    s = "#" + r + " " + g + " " + b;
    s = s.replace(" ", "");
    colors[i] = s.replace(" ", "");
}
console.log("New Data:")
console.log(source.data)
source.change.emit()

bar_data = bar_source.data;
console.log("BarChart data:");
console.log(bar_source.data);

bar_csv = bar_data['gene_list'];
console.log("bar_csv");
console.log(bar_csv);

selected_csv = bar_data['selected_csv'];
selected_csv = selected_csv[0];
console.log("selected_csv index");
console.log(selected_csv);

bar_csv = bar_csv[selected_csv];
console.log("selected_csv");
console.log(bar_csv);

time = slider.value;
console.log("slider value:");
console.log(time);

time = time - 1;

bar_csv = bar_csv[time];
console.log("final data");
console.log(bar_csv);

bar_counts = bar_data['counts'];

for (var i = 0; i < bar_counts.length; i++) {
    bar_counts[i] = bar_csv[i];
}

console.log("BarChart New data:");
console.log(bar_source.data);

bar_source.change.emit();
