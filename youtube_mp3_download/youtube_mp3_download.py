from pytube import YouTube

url = input('Cole aqui a URL: ')
yt = YouTube(url)

audio_stream = yt.streams.filter(only_audio=True).first()
print('Baixando...')
audio_stream.download()
print('Download concluído!')
