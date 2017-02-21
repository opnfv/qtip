import connexion


def main():
    app = connexion.App(__name__, specification_dir='api_specs/')
    app.add_api('specs.yaml', base_path='/v1.0')
    app.run(host='0.0.0.0', port='5000')


if __name__ == '__main__':
    main()
