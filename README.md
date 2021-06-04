# refgenie looper demo

This repo shows an example of how to use looper to populate refgenie registry paths automatically. The advantages are:

1. Pipelines don't have to know about refgenie
2. Users don't have to do anything other than supply a genome

Looper handles the part about getting the specific paths to specific assets for a provided genome, and then passing those along to the pipeline.

The magic happens in the `pipeline_interface.yaml` file

# The easy way (recommended)

1. Enable the refgenie looper plugin:

```
var_templates:
  refgenie_config: "$REFGENIE"
pre_submit:
  python_functions:
  - refgenconf.looper_refgenie_populate
 ```

This adds the refgenie looper plugin, which ships with refgenie, as a `pre_submit` hook. The `refgenie_config` is just the way you pass the refgenie file to the plugin.


2. Use refgenie in the command template:

All you have to do is refer to assets with `{refgenie.asset_name.seek_key}` in your command template!


```
command_template: >
  python pipeline.py 
  --index {refgenie.bowtie2_index.dir}
  --fasta-file {refgenie.fasta.fasta}
  --sample-name {sample.sample_name}
  --anno-name {refgenie.bwa_index.bwa_index}
```

If you need to change the tag of the asset, you do it in the project configuration file:

```
refgenie_asset_tags:
  bowtie2_index: tag_to_use
```

This is optional, refgenie will use the default tags if you don't provide them.



# The hard way (but it's more explicit)

1. Enable the refgenie looper plugin:

```
var_templates:
  refgenie_config: "$REFGENIE"
pre_submit:
  python_functions:
  - refgenconf.looper_refgenie_populate
 ```

This adds the refgenie looper plugin, which ships with refgenie, as a `pre_submit` hook. The `refgenie_config` is just the way you pass the refgenie file to the plugin.


2. Set up variables for any assets you need:


```
var_templates:
  bowtie2_index: "refgenie://{sample.genome}/bowtie2_index.dir"
  fasta_file: "refgenie://{sample.genome}/fasta"
```

Here, we set up refgenie registery paths, using the `{sample.genome}` attribute. These will then be available for...

3. Pass the variables to the pipeline in the command template:

```
command_template: >
  python pipeline.py 
  --index {pipeline.var_templates.bowtie2_index}
  --fasta-file {pipeline.var_templates.fasta_file}
  --sample-name {sample.sample_name}
 ```

Use `{pipeline.var_templates.bowtie2_index}` to get the populated refgenie path in your command template.# refgenie_looper_demo

The bad part about this method is that controlling the tags happens at the pipeline interface, and also you have to explicitly specify every asset you need to use in the command template.
