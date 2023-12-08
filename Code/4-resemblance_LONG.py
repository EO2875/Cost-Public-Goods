subgroups: list[pd.DataFrame] = []
for r in range(1,4): # Religion
    for l in range(1,4): # Language
        for p in range(1,4): # Phenotype
            group = epr_ed[[
                'gwid', 'gwgroupid',
                f'religion{r}', f'rel{r}_size', 
                f'language{l}', f'lang{l}_size', 
                f'phenotype{p}', f'pheno{p}_size'
            ]]
            group = group.dropna()
            group = group.rename(columns={
                f'religion{r}': 'rel', 
                f'rel{r}_size': 'rel_size', 
                f'language{l}': 'lang', 
                f'lang{l}_size': 'lang_size', 
                f'phenotype{p}': 'phenotype', 
                f'pheno{p}_size': 'pheno_size',
            })
            subgroups.append(group)

expanded_ethn = pd.concat(subgroups)
expanded_ethn.sort_values(['gwid', 'gwgroupid'], inplace=True)
expanded_ethn.to_csv('Try1.csv', index=False)