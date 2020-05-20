status.data.csv[0] = select.value;

const csv = status.data.csv[0];
const time = status.data.time[0] - 1;

const data = bar_source.data;

const time_series = data['gene_list'];

data['counts'] = time_series[csv][time];

bar_source.change.emit();
