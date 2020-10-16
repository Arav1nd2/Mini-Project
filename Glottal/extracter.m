dysarthric_speech_files = dir("./Audio/D/*.wav");
D_PATH = "./Audio/D/";
DO_PATH = "./Output/D/";

for file = dysarthric_speech_files'
    t_name = split(file.name, '.');
    name = string(t_name(1));
    disp(name)
    [y,Fs] = audioread(D_PATH + file.name);
    n = length(y);
    for k = 1:Fs:n
        try
            audioBlock = y(k:min(k + Fs - 1, n), :);
            % do something with this block
            if size(audioBlock,2)==1
              Y = signal(audioBlock,Fs);
            else
              for i=1:size(audioBlock,2)
                Y{i} = signal(audioBlock(:,i),Fs);
              end
            end
             qcp_options = struct;
             qcp_options.f0 = 70;
             flow = qcp(Y, qcp_options)

             time_params = glottaltimeparams(flow)
             freq_params = glottalfreqparams(flow)
             OP_folder = DO_PATH + name
             if ~exist(OP_folder, 'dir')
              mkdir(OP_folder);
              mkdir(OP_folder + '/time')
              mkdir(OP_folder + '/freq')
              mkdir(OP_folder + '/flow')
             end
             [t_rows, t_cols] = size(time_params);
             [f_rows, f_cols] = size(freq_params);
             if t_rows * t_cols ~= 0
                writetable(struct2table(time_params,'AsArray',true), OP_folder + '/time/' + int32(k / Fs) + '.csv');
             end
             if f_rows * f_cols ~= 0
                writetable(struct2table(freq_params,'AsArray',true), OP_folder + '/freq/' + int32(k / Fs) + '.csv');
             end
             sigwavwrite(flow, OP_folder + '/flow/' + int32(k/Fs) + '.wav'  )
        catch
            fprintf('Inconsistent data')
        end
    end
end


dysarthric_speech_files = dir("./Audio/ND/*.wav");
D_PATH = "./Audio/ND/";
DO_PATH = "./Output/ND/";

for file = dysarthric_speech_files'
    t_name = split(file.name, '.');
    name = string(t_name(1));
    disp(name)
    [y,Fs] = audioread(D_PATH + file.name);
    n = length(y);
    for k = 1:Fs:n
        try
            audioBlock = y(k:min(k + Fs - 1, n), :);
            % do something with this block
            if size(audioBlock,2)==1
              Y = signal(audioBlock,Fs);
            else
              for i=1:size(audioBlock,2)
                Y{i} = signal(audioBlock(:,i),Fs);
              end
            end
             qcp_options = struct;
             qcp_options.f0 = 70;
             flow = qcp(Y, qcp_options)

             time_params = glottaltimeparams(flow)
             freq_params = glottalfreqparams(flow)
             OP_folder = DO_PATH + name
             if ~exist(OP_folder, 'dir')
              mkdir(OP_folder);
              mkdir(OP_folder + '/time')
              mkdir(OP_folder + '/freq')
              mkdir(OP_folder + '/flow')
             end
             [t_rows, t_cols] = size(time_params);
             [f_rows, f_cols] = size(freq_params);
             if t_rows * t_cols ~= 0
                writetable(struct2table(time_params,'AsArray',true), OP_folder + '/time/' + int32(k / Fs) + '.csv');
             end
             if f_rows * f_cols ~= 0
                writetable(struct2table(freq_params,'AsArray',true), OP_folder + '/freq/' + int32(k / Fs) + '.csv');
             end
             sigwavwrite(flow, OP_folder + '/flow/' + int32(k/Fs) + '.wav')
        catch
            fprintf('Inconsistent data')
        end
    end
end
