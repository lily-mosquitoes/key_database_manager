import pymysql

class ModelDataset(object):

    def __init__(self, user, host, password):
        self._connection = pymysql.connect(
            host = host,
            user = user,
            password = password,
            db = 'key_database',
        )
        self.cursor = self._connection.cursor()

    @property
    def connection(self):
        return self._connection

    def _show_couplet_text(self, text, couplet):
        sql = "SELECT {} FROM couplet_data WHERE couplet_data.couplet = '{}';".format(text, couplet)
        try:
            self.cursor.execute(sql)
            text = self.cursor.fetchone()[0]
        except pymysql.Error as e:
            raise e
        return text

    def show_couplet(self, couplet):
        zero_text = self._show_couplet_text('zero_text', couplet)
        one_text = self._show_couplet_text('one_text', couplet)
        return zero_text, one_text

    def list_species(self):
        sql = """
        SHOW COLUMNS FROM species_states;
        """
        try:
            self.cursor.execute(sql)
            species = self.cursor.fetchall()
            species = [i[0] for i in species]
            species.remove('couplet')
        except pymysql.Error as e:
            raise e
        return species

    def list_couplets(self):
        sql = """
        SELECT couplet FROM species_states;
        """
        try:
            self.cursor.execute(sql)
            couplets = self.cursor.fetchall()
            couplets = [c[0] for c in couplets]
        except pymysql.Error as e:
            raise e
        return couplets

    def show_state(self, species, couplet):
        sql = """
        SELECT `{}` FROM species_states WHERE species_states.couplet = '{}';
        """.format(species, couplet)
        try:
            self.cursor.execute(sql)
            state = self.cursor.fetchone()[0]
        except pymysql.Error as e:
            raise e
        return state

    def update(self, species, value, couplet):
        if value != None:
            value = "'{}'".format(value)
        else:
            value = 'NULL'
        sql = """
        UPDATE `species_states`
        SET `{}` = {}
        WHERE `species_states`.`couplet` = '{}';
        """.format(species, value, couplet)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except pymysql.Error as e:
            self.connection.rollback()
            raise e
