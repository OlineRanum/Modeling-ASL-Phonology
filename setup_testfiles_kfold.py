import os

vers = ['T1', 'T2', 'T3']
m = '3'

views = ['r', 'f', 'l']
dir = 'NGT200/kfold_noanim'

for v in vers:
    method = m +'/' + v
    for view in views: 
        # Directory containing the .ckpt files
        ckpt_dir = 'new_models/'+dir+'/'+method+'/'
        # Path to the original config file
        orig_config_path = 'configs/'+dir+'/gcn_test.yaml'

        output_dir = 'configs/'+dir+'/'+method+'/'+ view +'/'
        
        if not os.path.exists('results/'+dir+'/'+method):
            os.makedirs('results/'+dir+'/'+method)
        if not os.path.exists('results/'+dir+'/'+method+'/'+ view +'/'):
            os.makedirs('results/'+dir+'/'+method+'/'+ view +'/')
            
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        def list_ckpt_files(directory):
            """List all .ckpt filenames in the directory."""
            return [f for f in os.listdir(directory) if f.endswith('.ckpt')]

        def modify_and_save_config(ckpt_files, original_config_path, output_dir):
            """Modify and save the config for each .ckpt file."""
            with open(original_config_path, 'r') as file:
                original_content = file.readlines()
            
            for i, ckpt_file in enumerate(ckpt_files, start=1):
                modified_content = []
                for line in original_content:
                    if line.strip().startswith('pretrained:'):
                        # Replace the pretrained model path
                        line = "pretrained: new_models/"+dir+"/"+method+f"/{ckpt_file}\n"
                    elif 'MODEL_NAME:' in line:
                        # Update MODEL_NAME
                        line = "        MODEL_NAME: &model_name "+m+f"_test_{i}\n"
                    elif 'OUTPUT_PATH:' in line:
                        # Update OUTPUT_PATH
                        line = "        OUTPUT_PATH: &output_path new_models/NGT200/"+method+"/" +view +"/\n"
                    elif 'DATA_PATH:' in line:
                        # Update DATA
                        line = "        DATA_PATH: &data_path training_data/NGT/metadata/kfold/test/"+v+"_"+view+".json\n"
                    elif 'RESULT_PATH:' in line:
                        # Update RESULT_PATH
                        line = "        RESULT_PATH: &result_path results/"+dir+"/"+method+"/"+view+"/"+f"_{i}.jsonl\n"
                    modified_content.append(line)
                
                # Save the modified config to a new file
                new_config_path = os.path.join(output_dir, f'test_modified_{i}.yml')
                with open(new_config_path, 'w') as new_file:
                    new_file.writelines(modified_content)
                
                print(f"Modified config saved to: {new_config_path}")

        # Get list of .ckpt files
        ckpt_files = list_ckpt_files(ckpt_dir)
        # Modify and save configs
        modify_and_save_config(ckpt_files, orig_config_path, output_dir)



        def modify_job_script(config_dir, original_job_script, modified_job_script):
            """
            Modifies the original runopenhands.job script by removing the existing srun command
            and adding multiple srun commands for each new config file, with paths matching
            the input config directory.
            
            Args:
            - config_dir: Directory containing the new config files, relative to the script execution or absolute.
            - original_job_script: Path to the original runopenhands.job Bash script.
            - modified_job_script: Path to save the modified runopenhands.job Bash script.
            """
            # List all config files in the directory
            config_files = [f for f in os.listdir(config_dir) if f.endswith('.yml')]
            
            # Read the original job script
            with open(original_job_script, 'r') as file:
                lines = file.readlines()
            
            # Identify and remove the line with the original srun command
            original_srun_line_index = None
            for i, line in enumerate(lines):
                if 'srun python' in line:
                    original_srun_line_index = i
                    break
            if original_srun_line_index is not None:
                del lines[original_srun_line_index]

            # Generate new srun commands with correct config paths
            new_srun_commands = []
            for config_file in config_files:
                config_path = os.path.join(config_dir, config_file)  # Correct path to config
                new_command = f"srun python $HOME/Modeling-ASL-Phonology/test.py {config_path}\n"
                new_srun_commands.append(new_command)
            
            # Insert new srun commands at the position of the original srun command
            modified_lines = lines[:original_srun_line_index] + new_srun_commands + lines[original_srun_line_index:]
            
            # Save the modified script to a new file
            with open(modified_job_script, 'w') as new_file:
                new_file.writelines(modified_lines)

            print(f"Modified job script saved to: {modified_job_script}")


        # Example usage:
        config_directory = output_dir
        original_job_script_path = 'runopenhands.job'
        modified_job_script_path = 'runopenhands_modified_'+v+'_' + m +view+'.job'
        modify_job_script(config_directory, original_job_script_path, modified_job_script_path)
