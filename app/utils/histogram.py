import matplotlib.pyplot as plt
import io
import base64


def generate_histogram(frequency_dict):
    plt.figure(figsize=(10, 6))
    plt.bar(frequency_dict.keys(), frequency_dict.values())
    plt.title('Histogram of Berry Growth Times')
    plt.xlabel('Growth Time')
    plt.ylabel('Frequency')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return graphic