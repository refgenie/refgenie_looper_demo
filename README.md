# refgenie looper demo

This repo shows an example of how to use looper to populate refgenie registry paths automatically. The advantages are:

1. Pipelines don't have to know about refgenie
2. Users don't have to do anything other than supply a genome

Looper handles the part about getting the specific paths to specific assets for a provided genome, and then passing those along to the pipeline. The magic happens in the `pipeline_interface.yaml` file

The looper system is super flexible and there are 3 different approaches you can use to get this done, depending on your needs.

1. This plugin provides a new `{refgenie}` namespace, which you can use directly in your command template.
2. You can specify refgenie registry paths to assets in `var_templates`, which will be populated by the plugin, and then can be used in your command template.
3. You can specify refgenie registry paths as sample attributes, which will be populated by the plugin, and then just use the sample attributes in your command template.


# Enable the plugin

For any of the 3 options, the first thing you have to do is enable the plugin in the looper `pipeline_interface.yaml`, which you do by adding this:

```
var_templates:
  refgenie_config: "$REFGENIE"
pre_submit:
  python_functions:
  - refgenconf.looper_refgenie_populate
 ```

This adds the refgenie looper plugin, which ships with refgenie, as a `pre_submit` hook. The `refgenie_config` setting passes the refgenie config file to the plugin.

# Use the plugin

## Option 1. Use refgenie in the command template (recommended)

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

# 2. Use var_templates (more work, but more explicit)

First, set up variables templates (`var_templates`) for any assets you need:

```
var_templates:
  bowtie2_index: "refgenie://{sample.genome}/bowtie2_index.dir"
  fasta_file: "refgenie://{sample.genome}/fasta"
```

Here, we set up refgenie registery paths, using the `{sample.genome}` attribute. These will then be available in your command template:

```
command_template: >
  python pipeline.py 
  --index {pipeline.var_templates.bowtie2_index}
  --fasta-file {pipeline.var_templates.fasta_file}
  --sample-name {sample.sample_name}
 ```

Use `{pipeline.var_templates.bowtie2_index}` to get the populated refgenie path in your command template.# refgenie_looper_demo

The bad part about this method is that controlling the tags happens at the pipeline interface, and also you have to explicitly specify every asset you need to use in the command template.

# 3. Use sample attributes

Finally, you could just stick a refgenie asset registry path as a sample attribute. You could just add it as a value in a column in your sample table, or do something like this using a derived column:

```
  derive:
    attributes: [read1, read2, Index, InputFile1, InputFile2]
    sources:
      FQ1: "data/{sample_name}_1.fq.gz"
      FQ2: "data/{sample_name}_2.fq.gz"
      RG1: "refgenie://{genome}/bwa_index"
```

Here, in the `Index` attribute we'd specify the value `RG1`, and this will get populated and can be used in your command template as `{sample.Index}`. Use this method if you need to specify different tags for each sample, because the above methods will expect you to provide the same tag across the board.
