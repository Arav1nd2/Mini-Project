[y, Fs] = audioread('./example1.wav')

if size(y,2)==1
    Y = signal(y,Fs);
else
    for i=1:size(y,2)
       Y{i} = signal(y(:,i),Fs);
    end
end

option = struct;
option.f0 = 70;
flow = qcp(Y, option);
sigwavwrite(flow, './flow.wav');