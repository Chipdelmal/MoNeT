// Bar
const csv = status.data.csv[0];
status.data.time[0] = slider.value;
const time = slider.value - 1;

const bar_data = bar_source.data;

const time_series = bar_data['gene_list'];
bar_data['counts'] = time_series[csv][time];

bar_source.change.emit();
// End bar

// Scatter
const scatter_data = source.data;

const colors = scatter_data['colors'];

scatter_data.count = timeList[time];


let min = Infinity, max = -Infinity;
scatter_data.count.forEach(element => {
    if (element < min) {
        min = element;
    } else if (element > max) {
        max = element;
    }
});

const hslToRgb = (h, s, l) => {
    let r, g, b;

    if (s == 0) {
        r = g = b = l; // achromatic
    } else {
        function hue2rgb(p, q, t) {
            if (t < 0) t += 1;
            if (t > 1) t -= 1;
            if (t < 1 / 6) return p + (q - p) * 6 * t;
            if (t < 1 / 2) return q;
            if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
            return p;
        }

        var q = l < 0.5 ? l * (1 + s) : l + s - l * s;
        var p = 2 * l - q;

        r = hue2rgb(p, q, h + 1 / 3);
        g = hue2rgb(p, q, h);
        b = hue2rgb(p, q, h - 1 / 3);
    }

    return [r * 255, g * 255, b * 255];
};


scatter_data.colors = scatter_data.count.map(e => {
    const val = (e - min) / (max - min);
    const rgb = hslToRgb(0.7, 0.5, 1 - val).map(c => Math.round(c).toString(16));
    const [r, g, b] = rgb;
    return '#' + r + g + b;
});

source.change.emit()
// End scatter