# Environmental Sensors

This project was created upon the need of the accurate logging of environmental field information for the creation of datasets that could feed into our [machine learning](./MachineLearning.html) project to predict mosquito population sizes in explicit landscapes. The general idea is to create a low-energy and low-cost device that is able to track weather factors that are known to correlate with the amount of mosquitos. Ideally, these devices could be attached to existing mosquito-counts setups (ovitraps, [sentinels](https://www.bg-sentinel.com/), etcetera).

## Requirements

* Low energy consumption
* Small size
* Robust to physical abuse (specify)

## Technical Specifications

* __Sampling Rate__: 24 (1/hour)
* __Resolution__:
  * __Humidity__: 1% RH
  * __Temperature__: ± 0.5 Centigrade
  * __Atmosferic Pressure__: 0.01 hPa
  * __Wind Direction & Speed__: .1 ms-1
* __Accuracy__:
  * __Humidity__: (proponemos ±5% RH)
  * __Temperature__: (proponemos ±5 °C)
  * __Atmosferic Pressure__: (proponemos ±1 hPa)
  * __Wind Direction & Speed__: (proponemos  1% ±0.1 ms-1)
* __Other__: Offline data dump to a flash drive (SD/micro SD Card)
* __Current Limitations__:
  * Needs wifi Access
  * 110 VAC power supply

<hr>

## Collaborators

* UC, Berkeley: <a href="https://chipdelmal.github.io/">Héctor M. Sánchez C.</a>, <a href="https://tomasleon.com/Tomás">Tomás León</a>, <a href="https://www.marshalllab.com/">John M. Marshall</a>
* ITESM: Camilo Duque

<!--
La idea que traemos el desarrollo de micro estaciones basadas en IoT de bajo costo para medición de variables ambientales (tales como humedad, temperatura, presión atmosférica, entre otras), las cuales tengan conectividad vía wifi para el almacenamiento de datos en la nube. Los usos potenciales de estas estaciones son variados y creo que pueden adecuarse al trabajo que ustedes desarrollan, ya que al ser de bajo costo y reducido tamaño, pueden instalarse en lugares urbanos que pueden ir cambiando en el tiempo según el interés del estudio que se este realizando, siendo la única limitante que haya acceso a internet wifi, lo cual, según me comentaste, es coincidente con algunos de los estudios que ustedes desarrollan.

Me gustaría que ustedes como usuarios que requieren la tecnología que estamos trabajando, tomen la iniciativa de los pasos a seguir, sin embargo y a reserva de lo que puedan proponer, sugiero nos compartan las especificaciones de las mediciones que ustedes necesitan, que variables, resolución, rangos, frecuencia de medición, entre otras características, con lo cual nosotros podremos adelantar requerimientos de diseño.-->
