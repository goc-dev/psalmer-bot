#!/usr/bin/env 

from pathlib import Path
import argparse
from telegramify_markdown import markdownify as MDify

def convert_md_to_mdv2( source_dir: Path, target_dir: Path) -> None:
    Path(target_dir).mkdir( parents=True, exist_ok=True)

    for file_path in Path(source_dir).iterdir():
        print('Source file: ', file_path)
        print('File suffix: ', file_path.suffix)
        if file_path.is_file() and file_path.suffix == '.md':
            with file_path.open('r', encoding='utf-8') as f_md:
                source_md = f_md.read()
                print('Source len:', len(source_md))
        
            target_mdV2 = MDify(source_md)
            print('Target len: ', len(target_mdV2))
            target_file = Path(f'{Path(target_dir) / file_path.name}V2')
            print('Target file: ', target_file)
            with target_file.open('w', encoding='utf-8') as f_mdV2:
                f_mdV2.write(target_mdV2)
            print(f'Converted: {file_path.name} -> {target_file}')
        else:
            print('Error:', file_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Convert Markdown files to MarkdownV2')
    parser.add_argument('--in-md'   , type=str, dest='in_md_path'   , required=True, help='Path to source Markdown')
    parser.add_argument('--out-mdv2', type=str, dest='out_mdv2_path', required=True, help='Path to target MarkdownV2')
    args = parser.parse_args()

    print('Parameters: ------')
    print( 'Source MD  : ', args.in_md_path)
    print( 'Target MDv2: ', args.out_mdv2_path)
    convert_md_to_mdv2( args.in_md_path, args.out_mdv2_path)
    