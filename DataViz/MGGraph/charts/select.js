console.log("Select List:");
console.log(select.value);
console.log(select.options);
select_opt = select.options;
var index = 0;
for (var i = 0; i < select_opt.length; i++) {
    if (select_opt[i] == select.value) {
        index = i;
    }
}
console.log("Index Value");
console.log(index);

bar_data = bar_source.data;
console.log("BarChart data:");
console.log(bar_source.data);

bar_csv = bar_data['gene_list'];
console.log("bar_csv");
console.log(bar_csv);

selected_csv = bar_data['selected_csv'];
selected_csv = selected_csv[index];
console.log("selected_csv index");
console.log(selected_csv);

bar_csv = bar_csv[index];
console.log("selected_csv");
console.log(bar_csv);

time = bar_data['selected_time'];
time = time[0];
console.log("time: ");
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
