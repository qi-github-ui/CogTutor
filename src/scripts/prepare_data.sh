python -m src.cogtutor.prepare_datashop --config configs/data_paths.yaml
python -m src.cogtutor.build_domain_model --config configs/data_paths.yaml
python -m src.cogtutor.make_cogtutor_corpus --config configs/data_paths.yaml
