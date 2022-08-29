from systems.plugins.index import BaseProvider


class Provider(BaseProvider('field_processor', 'growth_ratio')):

    def exec(self, dataset, field_data, compare_column):
        return (field_data / dataset[compare_column]) * 100
