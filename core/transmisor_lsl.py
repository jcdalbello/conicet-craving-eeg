from pylsl import StreamInfo, StreamOutlet


class TransmisorLSL:
    def __init__(self, nombre_del_stream: str):
        info = StreamInfo(
            name = nombre_del_stream,
            type = 'Markers',
            channel_count = 1,
            nominal_srate = 0,
            channel_format = 'string',
            source_id = 'exp_psico_01'
        )
        self.outlet_lsl = StreamOutlet(info)

    def enviar_trigger(self, trigger: str):
        self.outlet_lsl.push_sample([trigger])
