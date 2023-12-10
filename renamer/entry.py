from pathlib import Path
from typing import Sequence

import libcst


class RenameTransformer(libcst.CSTTransformer):
    def __init__(self, old_name: str, target_name: str):
        super().__init__()
        self._old_name = old_name
        self._target_name = target_name
        self._restore_keywords = []

    def _rename(self, original_node, renamed_node):
        if original_node.value == self._old_name:
            return renamed_node.with_changes(value=self._target_name)
        else:
            return renamed_node

    def leave_Name(self, original_node, renamed_node):
        return self._rename(original_node, renamed_node)


class CodeRenamer:
    """
    Tool to rename classes, functions, variables, arguments

    Works for filepaths and directories.
    """
    def __init__(self, path: str):
        self.path = Path(path)

    def rename_variable(self, old_name: str, target_name: str):
        for file in self._get_files():
            res = self._rename_var(
                file.read_text(),
                old_name,
                target_name
            )

            return res  # just for testing, actually supposed to save renamed files near to source files
            # if res:
            #     with open(file.parent / ('renamed_' + file.name), "w") as file:
            #         file.write(res)

    def _get_files(self) -> list[Path]:
        file_list = []
        if self.path.is_dir():  # if self.path is path to directory
            for p in self.path.glob("*"):
                if p.name[-3:] == '.py':
                    file_list.append(self.path / p.name)
        else:  # if self.path is path to file
            file_list.append(self.path)
        return file_list

    @staticmethod
    def _rename_var(source_code: str, old_name: str, target_name: str) -> str:
        rename_transformer = RenameTransformer(old_name, target_name)
        original_tree = libcst.parse_module(source_code)
        renamed_tree = original_tree.visit(rename_transformer)
        return renamed_tree.code if not original_tree.deep_equals(renamed_tree) else False


class AddImport(libcst.CSTTransformer):
    def __init__(self, add_code: libcst.CSTNode | Sequence[libcst.CSTNode]) -> None:
        super().__init__()
        self._code_to_add = add_code

    def leave_SimpleStatementLine(
        self, original_node: libcst.SimpleStatementLine, updated_node: libcst.SimpleStatementLine
    ) -> libcst.BaseStatement | libcst.FlattenSentinel[libcst.BaseStatement] | libcst.RemovalSentinel:
        if isinstance(updated_node, libcst.SimpleStatementLine) and isinstance(updated_node.body[0], libcst.Import):
            return libcst.FlattenSentinel([updated_node] + list(self._code_to_add))
        return updated_node


class ClassOrFuncMover:
    """
    Moves either class or function to another file and deletes it from the source code.
    """
    def __init__(self, path: str, new_path: str):
        self.path = Path(path)
        self.new_path = Path(new_path)  # new filepath to store moved class or func
        self.res = libcst.parse_module(self.path.read_text())

    def move(self, element_name: str, element_type_str: str):
        """
        Provide element_type_str as 'class' or 'func' to choose moving mode (type of moving element).
        """
        if element_type_str == 'class':
            element_type = libcst.ClassDef
        elif element_type_str == 'func':
            element_type = libcst.FunctionDef
        else:
            raise Exception('No such element type. Available types: "class", "func".')
        for element in self.res.body:
            if isinstance(element, element_type) and element.name.value == element_name:
                new_code = libcst.Module([element.deep_clone()])
                # with open(self.new_path, "w") as file:
                #     file.write(new_code.code)

                old_code = self.res.deep_remove(element)
                old_code = self.fix_import(old_code, self.new_path.stem, element_name)
                # with open(self.path.parent / ('modified_func_' + self.path.name), "w") as file:
                #     file.write(old_code.code)

                return new_code.code, old_code.code

    @staticmethod
    def fix_import(node: libcst.CSTNode, path_name: str, func_name: str):
        """Adds import line with the element to the code"""
        to_add = libcst.parse_module(f'from {path_name} import {func_name}').body
        updated_cst = node.visit(AddImport(to_add))

        return updated_cst

