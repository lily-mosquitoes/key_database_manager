import pymysql


class ModelDataset(object):

    def __init__(self, **kwargs):
        self._connection = pymysql.connect(**kwargs)
        self.cursor = self._connection.cursor()

        # cache species names
        self.db_species = self._list_species()

        # cache couplet info
        cp_info = self._get_couplet_info()
        self.db_couplets = list()
        self._cp_cache = dict()
        for couplet, z, o in cp_info:
            self.db_couplets.append(couplet)
            self._cp_cache[couplet] = (z, o)

    @property
    def connection(self):
        return self._connection

    def _get_couplet_info(self):
        sql = """
            SELECT couplet, zero_text, one_text FROM couplet_data;
        """
        try:
            self.cursor.execute(sql)
            info = self.cursor.fetchall()
        except pymysql.Error as e:
            raise e
        return info

    def show_couplet(self, couplet):
        zero_text, one_text = self._cp_cache[couplet]
        return zero_text, one_text

    def _list_species(self):
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
        # input validation
        if species in self.db_species and couplet in self.db_couplets:
            pass
        else:
            raise pymysql.IntegrityError
        #
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
        # input validation
        if value != None and value in ['0', '1', '01', '10', 'NA']:
            value = "'{}'".format(value)
        elif value == None or value == 'NULL':
            value = 'NULL'
        else:
            raise pymysql.IntegrityError
        #
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

    def change_my_password(self, text):
        if len(text) >= 8:
            sql = """
                SET PASSWORD = %s;
            """
            params = [text]
            try:
                self.cursor.execute(sql, params)
                self.connection.commit()
            except pymysql.Error as e:
                self.connection.rollback()
                raise e
        else:
            raise pymysql.IntegrityError('passwords must be at least 8 characters long')
